from flask import Flask, render_template, request
from src import algorithm

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chart/", methods=['POST'])
def new_index():
    stock = request.form['stock']
    portfel = request.form['portfel']
    period = request.form['period']
    algorithm.make_graph(stock, portfel, period)
    return render_template('index.html', url='/static/images/plot.png')

@app.route("/create_acc/")
def create_account():
    return render_template('log_acc.html')

if __name__ == '__main__':
    app.run(debug = True)
