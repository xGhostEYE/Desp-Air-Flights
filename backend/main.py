from flask import Flask

backend = Flask(__name__)

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

def main():
  return "It Works!"

if __name__ == '__main__':
  backend.run(debug=True)

@backend.route("/airports")
def get_airports():
  return jsonify(airports)