from flask import Flask
from flask import render_template, request, json
from flask import jsonify
# from models import test
from root.database.models import test
# from flask.ext.cors import CORS

app = Flask(__name__)
# CORS(app)

score = {
    "NE": 100,
    "E1": 250,
    "E2": 500,
    "E3": 750
}

limit = {
    "NE": 10*score["NE"],
    "E1": 10*score["E1"],
    "E2": 10*score["E2"],
    "E3": 10*score["E3"]
}

increment = {
    "E1": 50,
    "E2": 100,
    "E3": 150
}

#dummy endpoint to test if flask is working
@app.route("/")
def hello():
    dummy_data = {"status": True}
    return jsonify(dummy_data)


@app.route("/signup", methods=['POST'])
def signup():
    """
    receive: signup data from user 
    return: profile + credit-bucket of the user
    """
    if request.method == "POST":
        data = request.get_json()
        # read if user already exists.
        # send data back saying user already exists.
        # create user details in mongo DB
        promo = data.get("promo", "")
        if promo:
            # check for the promo code table in Mongo DB
            # if promo code does not exist, send back invalid promo code to user
            # fetch bucket of the from user email and validate current email with to email.
            # if email is invalid, show error test.
            # if bucket is  NE:
                # skip
            # increment score of the referrer and referee (score + increment[bucket])
            # update the bucket if needed comparing the score
        else:
            # feed the data to random forest and get the bucket
            # assign the min. score corresponding to the bucket.
            # save it to the db. return the bucket, credit score and bucket timelines.
        dummy_data = {"signup_status": True}
        return jsonify(dummy_data)

@app.route("/signin", methods=['POST'])
def signin():
    """
    receive: sigin credentials 
    return: profile + credit-bucket of the user
    """
    if request.method == 'POST':
        data = request.get_json()
        # go to DB and fetch the eligibility bucket
        return jsonify({"a": "hello"})

@app.route("/avail_credit", methods=['POST','GET'])
def avail_credit():
    if request.method == 'POST':
        data = request.get_json()
        # go to DB and update timestamp and credit amount
        return jsonify({"a": "hello"})
    elif request.method == 'GET':
        email = request.args.get("email")
        # go to db and fetch bucket and credit amount
        # limit[bucket]-credit and send it back as JSON

@app.route("/pay_dues", methods=['POST', 'GET'])
def pay_dues():
    if request.method == 'POST':
        data = request.get_json()
        # Update credit amount in db (credit = credit - payment)
        # read timestamp + config from DB. If current timestamp > X, 
        # decrement referr's and referres credit score. Recalculate buckets.'
        return jsonify({"a": "hello"})
    elif request.method == 'GET':
        email = request.args.get("email")
        # credit amount and due date (config + timestamp) from DB
        # send it to react

@app.route("/referral", methods=['POST'])
def referral():
    if request.method == 'POST':
        data = request.get_json()
        # email, verify the email id, if wrong show invalid.
        # create entry with referral code of the referrer inside referral table along with email ids.
        return jsonify({"a": "hello"})

if __name__ == "__main__":
    app.run()