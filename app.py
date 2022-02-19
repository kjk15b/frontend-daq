from termios import XTABS
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

colors = {'UR' : 'green',
              'UL' : 'blue',
              'LR' : 'red',
              'LL' : 'purple'}
                            

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
        if len(dataStream[sensor]) > 100:
            dataStream[sensor].pop(0)
        dataStream[sensor].append(value)
        return "{},{}".format(sensor, value)
    return "Nothing to see here"

@app.route('/plot/<sensor>')
def plotSensor(sensor):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Raw Feed: {}".format(sensor))
    axis.set_xlabel("Samples")
    axis.set_ylabel("Raw Feed")
    xs = range(len(dataStream[sensor]))
    #print(XTABS)
    axis.plot(xs, dataStream[sensor], color=colors[sensor])
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

if __name__ == '__main__':
    app.run(debug=sys.argv[1], host=sys.argv[2],
    port=sys.argv[3])