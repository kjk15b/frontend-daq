from flask import Flask, request
import sys

dataStream = {'UR' : list(),
              'UL' : list(),
              'LR' : list(),
              'LL' : list()}

app = Flask(__name__)

@app.route('/data/ingest/<sensor>', methods=['POST'])
def ingestRoute(sensor):
    if request.method == "POST":
        data = request.form.to_dict()
        value = data['data']
        print("received: {}, value={}".format(sensor, value))
        if len(dataStream[sensor]) > 5:
            dataStream[sensor].pop(0)
        dataStream[sensor].append(value)

if __name__ == '__main__':
    app.run(debug=sys.argv[1], host=sys.argv[2],
    port=sys.argv[3])