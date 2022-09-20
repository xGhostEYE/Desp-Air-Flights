from flask import Flask

backend = Flask(__name__)
@backend.route("/")
def main():
  return "It Works!"
if __name__ == '__main__':
  backend.run(debug=True)