from flask import Flask, render_template
from src import algorithm

app = Flask(__name__)

@app.route('/')
def index():
    algorithm.make_graph()
    return render_template('index.html', url='/static/images/plot.png')

if __name__ == '__main__':
    app.run()
