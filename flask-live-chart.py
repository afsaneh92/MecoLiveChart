import json
import sqlite3
from time import time
import psutil
from flask import Flask, render_template, make_response
from bar_graph import create_plot

app = Flask(__name__)


@app.route("/data.json")
def data():
    connection = sqlite3.connect("db.sqlite")
    cursor = connection.cursor()
    cursor.execute("SELECT 1000*timestamp, measure from measures")
    results = cursor.fetchall()
    print(results)
    return json.dumps(results)


@app.route("/graph")
def graph():
    return render_template('graph.html')


@app.route('/')
def hello_world():
    mem = psutil.virtual_memory()
    # bar chart
    bar = create_plot(mem)
    # pie chart
    data = {'Memory': 'bytes', 'total': mem.total, 'available': mem.available, 'used': mem.used, 'free': mem.free}

    return render_template('index.html', data=data, plot=bar)

    # return render_template('index.html', data='test')


@app.route('/live-data')
def live_data():
    # Create a PHP array and echo it as JSON
    data = [time() * 1000, psutil.cpu_percent()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
