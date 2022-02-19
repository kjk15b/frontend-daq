from flask import Flask, request, render_template, send_file, make_response
import sys
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
#import numpy as np

dataStream = {'UR' : list(),
              'UL' : list(),
              'LR' : list(),
              'LL' : list()}

app = Flask(__name__)

@app.route('/', methods=["GET"])
def homepage():
    return render_template('homepage.html')

@app.route('/data/ingest/<sensor>', methods=['POST'])
def ingestRoute(sensor):
    if request.method == "POST":
        data = request.form.to_dict()
        value = data['data']
        print("received: {}, value={}".format(sensor, value))
        if len(dataStream[sensor]) > 5:
            dataStream[sensor].pop(0)
        dataStream[sensor].append(value)
        return "{},{}".format(sensor, value)
    return "Nothing to see here"

@app.route('/plot/UR')
def plotSensor():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Raw Feed: UR")
    axis.set_xlabel("Samples")
    axis.set_ylabel("Raw Feed")
    xs = range(len(dataStream['UR']))
    print(xs)
    axis.plot(xs, dataStream['UR'])
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

if __name__ == '__main__':
    app.run(debug=sys.argv[1], host=sys.argv[2],
    port=sys.argv[3])