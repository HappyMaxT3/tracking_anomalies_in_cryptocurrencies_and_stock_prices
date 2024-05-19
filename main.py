from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from src import algorithm, password_generator

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anomaly_detection.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    # monitored_stocks = db.Column(db.String(255), lazy=True)

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock = request.form['stock']
        portfel = request.form['portfel']
        period = request.form['period']
        algorithm.make_graph(stock, portfel, period)
        if request.form.get('checkbox') == 'on':
            if session.get('user_id'):
                print("You will receive notice about notifications on id ", session.get('user_id'))
            else:
                return redirect(url_for("log_in_account"))
        return render_template('index.html', url='/static/images/plot.png')
    return render_template('index.html')

@app.route("/login/", methods=['GET', 'POST'])
def log_in_account():
    if session.get('user_id'):
        return redirect(url_for("profile"))
    if request.method == 'POST':
        email_adress = request.form['email_adress']
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
    if request.method == 'POST':
        if user_id:
            db.session.delete(user)
            db.session.commit()
            session.pop('user_id', None)
        return redirect(url_for("index"))

    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_email = user.email
    return render_template("your_acc.html", your_email=user_email)

@app.route("/create_account/", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email_adress = request.form['email_adress']
        password = password_generator.generate()
        new_user = User(email=email_adress, password=password)
        print(email_adress, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("log_in_account"))
    return render_template("create_acc.html")

if __name__ == '__main__':
    app.run(debug=True)