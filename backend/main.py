from flask import Flask, jsonify
from flask_cors import CORS

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# test data:
airports = [
    { 
      'city': 'Saskatoon', 
      'code': 'YXE' 
    },
    { 
      'city': 'Regina',
      'code': 'YQR'
    }
]

flights = [
  {
    'flight1': {
      'departure': {
        'location': 'Saskatoon',
        'time': '2022-12-10T13:45:00.000Z',
        'airport code': 'YXE'
      },

      'arrival': {
        'location': 'Regina',
        'time': '2022-12-10T16:20:00.000Z',
        'airport code': 'YQR'
      } 
    }
  }
]

@app.route("/flights", methods=['GET'])
def get_flight():
  return jsonify(flights)

@app.route("/airports", methods=['GET'])
def get_airports():
  return jsonify(airports)


if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')

