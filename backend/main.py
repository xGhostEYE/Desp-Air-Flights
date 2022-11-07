from flask import Flask, jsonify, request
from flask_cors import CORS
import search
from search import find_path as fp

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


@app.route("/flights", methods=['GET'])
def get_flight():
  return jsonify(fp.get_paths_json(
    request.args.get("departure", default="", type=str),
    request.args.get("destination", default="", type=str)
))

@app.route("/airports", methods=['GET'])
def get_airports():
  return jsonify(airports)


if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')

