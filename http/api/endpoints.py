from flask import Flask
app = Flask(__name__)

#dummy endpoint to test if flask is working
@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()