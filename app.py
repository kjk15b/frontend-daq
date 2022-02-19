from flask import Flask 
import sys

dataStream = {'UR' : list(),
              'UL' : list(),
              'LR' : list(),
              'LL' : list()}

app = Flask(__name__)

@app.route('/data/ingest/<sensor>/<value>')
def ingestRoute(sensor, value):
    value = int(value)
    print("received: {}, value={}".format(sensor, value))
    if len(dataStream[sensor]) > 5:
        dataStream[sensor].pop(0)
    dataStream[sensor].append(value)

if __name__ == '__main__':
    app.run(debug=sys.argv[1], host=sys.argv[2],
    port=sys.argv[3])