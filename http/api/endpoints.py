from flask import Flask
from flask import jsonify
from models import test
from ..models1 import test

app = Flask(__name__)

#dummy endpoint to test if flask is working
@app.route("/")
def hello():
    """
    """
    dummy_data = {"status": True}
    return jsonify(dummy_data)


@app.route("/signup")
def signup():
    """
    receive: signup data from user 
    return: profile + credit-bucket of the user
    """
    dummy_data = {"signup_status": True}
    return jsonify(dummy_data)


@app.route("/signin")
def signin():
    """
    receive: sigin credentials 
    return: profile + credit-bucket of the user
    """
    dummy_data = {"signin_status": True}
    return jsonify(dummy_data)


if __name__ == "__main__":
    app.run()
