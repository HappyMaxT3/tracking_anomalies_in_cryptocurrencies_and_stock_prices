from flask import Flask, render_template, request, redirect, url_for, session
from src import algorithm

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock = request.form['stock']
        portfel = request.form['portfel']
        period = request.form['period']
        algorithm.make_graph(stock, portfel, period)
        return render_template('index.html', url='/static/images/plot.png')
    return render_template('index.html')

@app.route("/login/", methods=['GET', 'POST'])
def log_in_account():
    if session.get('active') == '1':
        return redirect(url_for("profile"))
    if request.method == 'POST':
        email_adress = request.form['email_adress']
        password = request.form['password']
        session['active'] = '1'
        return redirect(url_for("index"))
    return render_template('log_acc.html')

@app.route("/profile/", methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        session.pop('active', None)
        return redirect(url_for("index"))
    return render_template("your_acc.html")

@app.route("/create_account/", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email_adress = request.form['email_adress']
        return redirect(url_for("log_in_account"))
    return render_template("create_acc.html")

if __name__ == '__main__':
    app.run(debug = True)
