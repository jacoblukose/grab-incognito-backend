from flask import Flask
from flask import jsonify

app = Flask(__name__)

#dummy endpoint to test if flask is working
@app.route("/")
def hello():
    dummy_data = { "status" : True}
    return jsonify(dummy_data)


if __name__ == "__main__":
    app.run(host= '0.0.0.0')