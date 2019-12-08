from flask import Flask
from flask import render_template, request, json
from flask import jsonify
# from models import test
# from root.database.models import test
# from flask.ext.cors import CORS
from root.database.mongodb.mongoclient import MongoClientWrapper
from root.utils.hash-me.py import getHashedValue
import time

app = Flask(__name__)
# CORS(app)

dueTime = 60000

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

referral = {
    "E1" : "NE",
    "E2" : "E1"
    "E3" : "E2"
}

def updateBucket(creditScore):
    if creditScore > score["E3"]:
        return "E3"
    elif creditScore > score["E2"]:
        return "E2"
    elif creditScore > score["E1"]:
        return "E1"
    else return "NE"

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
        email = {"email": data['email_id']}
        result = MongoClientWrapper().read(email, 'user_test')
        print(result)
        if result:
            msg = {"status": False, "text" : "User Data already Exists. Please try with an alternative Email Id"}
            return jsonify(msg)
        referral_code = data.get("referral_code", "")
        if referral_code:
            query = {"referral_code":referral_code, "to_email": email}
            obj = MongoClientWrapper().read(query, 'referral_test')
            print(obj)
            if obj:
                from_email = obj['from_email']
                result = MongoClientWrapper().read(from_email, 'user_test')
                referrer_credit_score = increment[result["bucket"]] + result["credit_score"]
                referrer_bucket = updateBucket(referrer_credit_score)
                query = {'email':from_email}
                values = { "$set": { "credit_score": referrer_credit_score, "bucket": referrer_bucket } }
                m.update(query, values, 'user_test' )
                # result = MongoClientWrapper().read(email, 'user_test')
                referree_credit_score = increment[result["bucket"]] + result["credit_score"]
                referree_bucket = updateBucket(referrer_credit_score)
                # query = {'email':email}
                # values = { "$set": { "credit_score": referree_credit_score, "bucket": referree_bucket } }
                # m.update(query, values, 'user_test' )
                # Update Graph
            else:
                msg = {"status": False, "text" : "Invalid Referral Code"}
                return jsonify(msg)
        # else:
            # feed the data to random forest and get the bucket
            # assign the min. score corresponding to the bucket.
            # save it to the db. return the bucket, credit score and bucket timelines.
        data['referral_code'] = getHashedValue(email, 6)
        data["credit_score"] = referree_credit_score
        data["bucket"] = referree_bucket
        MongoClientWrapper().write(data,  'user_test')
        msg = {"status": True, data: data}
        return jsonify(msg)

@app.route("/signin", methods=['POST'])
def signin():
    """
    receive: sigin credentials 
    return: profile + credit-bucket of the user
    """
    if request.method == 'POST':
        data = request.get_json()
        result = MongoClientWrapper().read(data, 'user_test')
        if result:
            msg = {"status": True, data: result}
            return jsonify(msg)
        else:
            msg = {"status": False, "text" : "Invalid Credentials, Please try again"}
            return jsonify(msg)

@app.route("/avail_credit", methods=['POST','GET'])
def avail_credit():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email_id']
        total_credit = data['credit_amount']
        query = {'email': email}
        values = { "$set": { "total_credit": total_credit, "credit_amount": total_credit,  "timestamp": time.time } }
        m.update(query, values, 'user_test' )
    elif request.method == 'GET':
        email = request.args.get("email_id")
        result = MongoClientWrapper().read({"email": email}, 'user_test')
        limit = limit[result["bucket"]] - result['credit_amount']
        return jsonify({"limit": limit})

@app.route("/pay_dues", methods=['POST', 'GET'])
def pay_dues():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email_id']
        result = MongoClientWrapper().read({"email": email}, 'user_test')
        credit_amount = result['credit_amount'] - data['payment']
        if time.time > result['timestamp'] + dueTime:
            if not result['referrerActionTaken']:
                ref_email = result['referredBy']
                result2 = MongoClientWrapper().read({"email": ref_email}, 'user_test')
                query = {'email': ref_email}
                credit_score = result2['credit_score'] - increment[result2['bucket']]
                bucket = updateBucket(credit_score)
                values = { "$set": { "credit_score": credit_score, "bucket": bucket } }
                m.update(query, values, 'user_test' )
            credit_score = result['credit_score'] - increment[result['bucket']]
            bucket = updateBucket(credit_score)
            query = {'email': email}
            values = { "$set": { "credit_score": credit_score, "bucket": bucket } }
            m.update(query, values, 'user_test' )
    elif request.method == 'GET':
        email = request.args.get("email_id")
        result = MongoClientWrapper().read({"email": email}, 'user_test')
        due_amount = result['credit_amount']
        due_time = result['timestamp'] + dueTime
        return jsonify({"due_amount": due_amount, "due_time": due_time})

@app.route("/referral", methods=['POST'])
def referral():
    if request.method == 'POST':
        data = request.get_json()
        to_email = data['to_email']
        from_email = data['from_email']
        result1 = MongoClientWrapper().read({"email": from_email}, 'user_test')
        result2 = MongoClientWrapper().read({"email": to_email}, 'user_test')
        if result1 and result2:
            referral_code = result1['referral_code']
            data["referral_code"] = referral_code
            MongoClientWrapper().write(data,  'referral_test')
            query = {'email': to_email}
            values = { "$set": { "referredBy": to_email, "referrerActionTaken": False } }
            m.update(query, values, 'user_test' )
            msg = {"status": True, "text" : "Referral Sent!"}
            return jsonify(msg)
        else:
            msg = {"status": False, "text" : "Invalid Email Id Entered, Please try again"}
            return jsonify(msg)

if __name__ == "__main__":
    app.run()