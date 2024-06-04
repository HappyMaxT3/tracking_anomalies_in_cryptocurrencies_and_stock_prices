from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.dialects.postgresql import JSON
from src import algorithm, password_generator
import json
import yfinance as yf
import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anomaly_detection.db'
db = SQLAlchemy(app)
scheduler = BackgroundScheduler()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'trackinganomalies@gmail.com'
app.config['MAIL_PASSWORD'] = 'kvcn thxh zmim cmol'
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    monitored_stocks = db.Column(JSON)

with app.app_context():
    db.create_all()
    
def fetch_and_detect_anomalies():
    print('----------------------- Background task executed -----------------------')
    users = User.query.all()
    for user in users:
        for i in user.monitored_stocks:
            stock, portfel = i.split(',')
            type_of_anomaly = algorithm.detect_anomalies(stock, portfel)
            if type_of_anomaly in ['fallen', 'increased']:
                msg = Message('Anomaly detected', sender='trackinganomalies@gmail.com', recipients=user.email)
                msg.body = f'Anomaly was detected in {stock}. The share price has {type_of_anomaly}.'
                mail.send(msg)
    
    
def send_password(email, password):
    msg = Message('Your Account Password', sender='trackinganomalies@gmail.com', recipients=[email])
    msg.body = f'Your password: {password}'
    mail.send(msg)

@app.route("/", methods=['GET', 'POST'])
def index():
    formatted_news = []
    anomalies = []
    error_message = None

    if request.method == 'POST':
        stock = request.form['stock']
        portfel = f"^{request.form['portfel']}"
        period_start = request.form['period_start']
        period_end = request.form['period_end']
        
        news = yf.Ticker(stock).news
        for news_item in news:
            timestamp = int(news_item['providerPublishTime'])
            formatted_date = datetime.datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M')
            formatted_news.append({
                'title': news_item['title'],
                'publisher': news_item['publisher'],
                'link': news_item['link'],
                'formatted_date': formatted_date
            })
        
        try:
            anomalies = algorithm.make_graph(stock, portfel, period_start, period_end)
        except RuntimeError as e:
            error_message = str(e)
        
        if request.form.get('checkbox') == 'on':
            user_id = session.get('user_id')
            if user_id:
                user = User.query.get(user_id)
                monitored_stocks = json.loads(user.monitored_stocks) if user.monitored_stocks else []
                monitored_stocks.append({'stock': stock, 'portfel': portfel})
                user.monitored_stocks = json.dumps(monitored_stocks)
                db.session.commit()
                print("Updated monitored_stocks for user with id ", user_id)
            else:
                return redirect(url_for("log_in_account"))

    return render_template('index.html', url='/static/images/plot.png', news=formatted_news, anomalies=anomalies, error_message=error_message)


@app.route("/login/", methods=['GET', 'POST'])
def log_in_account():
    if session.get('user_id'):
        return redirect(url_for("profile"))
    if request.method == 'POST':
        email_adress = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email_adress, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password", "error")
    return render_template('log_acc.html')

@app.route("/profile/", methods=['GET', 'POST'])
def profile():
    user = User.query.get(session.get('user_id'))
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
            session.pop('user_id', None)
        return redirect(url_for("index"))

    user_email = user.email
    return render_template("your_acc.html", your_email=user_email)

@app.route("/create_account/", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email_adress = request.form['email_adress']
        password = password_generator.generate()
        new_user = User(email=email_adress, password=password, monitored_stocks=[])
        send_password(email_adress, password)
        print(email_adress, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("log_in_account"))
    return render_template("create_acc.html")

def scheduled_fetch_data():
    with app.app_context():
        fetch_and_detect_anomalies()

# scheduler.add_job(func=scheduled_fetch_data, trigger='interval', seconds=15, id='fetch_data_job')
#scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)