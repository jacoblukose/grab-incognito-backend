from flask import Flask
from flask import render_template, request, json
from flask import jsonify
# from models import test
# from root.database.models import test
# from flask.ext.cors import CORS
from root.database.mongodb.mongoclient import MongoClientWrapper
from root.utils.hash_me import getHashedValue
from root.models.new_user_classifier.model import run_model_inference
import time
from datetime import date
import datetime

app = Flask(__name__)
# CORS(app)

dueTime = 60000




score = {
    "NE": 100,
    "E1": 250,
    "E2": 500,
    "E3": 750
}

limit1 = {
    "NE": 0*score["NE"],
    "E1": 10*score["E1"],
    "E2": 10*score["E2"],
    "E3": 10*score["E3"]
}

increment = {
    "E1": 50,
    "E2": 100,
    "E3": 150
}

referral_ = {
    "E1" : "NE",
    "E2" : "E1",
    "E3" : "E2"
}

def calculate_age(born):
    today = date.today()
    return today.year - int(born['year']) - ((today.month, today.day) < (int(born['month']), int(born['day'])))

def updateBucket(creditScore):
    if creditScore > score["E3"]:
        return "E3"
    elif creditScore > score["E2"]:
        return "E2"
    elif creditScore > score["E1"]:
        return "E1"
    else:
        return "NE"

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
        print(data)
        email = {"email_id": data['email_id']}
        result = MongoClientWrapper().read(email, 'user_test')
        for i in result:
            msg = {"status": False, "text" : "User Data already Exists. Please try with an alternative Email Id"}
            return jsonify(msg)
        referral_code = data.get("referral_code", "")
        if referral_code:
            print(referral_code)
            print("dfsdf")
            query = {"referral_code":int(referral_code), "to_email": data['email_id']}
            obj = MongoClientWrapper().read(query, 'referral_test')
            X = True
            for j in obj:
                X = False
                from_email = {"email_id": j['from_email']}
                result = MongoClientWrapper().read(from_email, 'user_test')
                for i in result:
                    referrer_credit_score = increment[i["bucket"]] + i["credit_score"]
                    referrer_bucket = updateBucket(referrer_credit_score)
                    query = {'email_id':from_email}
                    values = { "$set": { "credit_score": referrer_credit_score, "bucket": referrer_bucket } }
                    MongoClientWrapper().update(query, values, 'user_test' )
                    # result = MongoClientWrapper().read(email, 'user_test')
                    # print(i["bucket"])
                    # print(increment[i["bucket"]])
                    # print(referral[i["bucket"]])
                    # print(score[referral[i["bucket"]]])
                    referree_credit_score = increment[i["bucket"]] + score[referral_[i["bucket"]]]
                    referree_bucket = updateBucket(referrer_credit_score)
                    data['referral_code'] = getHashedValue(data['email_id'], 6)
                    data["credit_score"] = referree_credit_score
                    data["bucket"] = referree_bucket
                    data["credit_amount"] = 0
                    data["timestamp"] = 0
                # query = {'email':email}
                # values = { "$set": { "credit_score": referree_credit_score, "bucket": referree_bucket } }
                # m.update(query, values, 'user_test' )
                # Update Graph
            print(X)
            print("dfasd")
            if X:
                msg = {"status": False, "text" : "Invalid Referral Code"}
                return jsonify(msg)
        else:
            #age, latitude, logituede, gender, marital status, occupation
            print(data)
            print("sdfasdf")
            age = calculate_age({ 'year':data['dob'][:4], 'month':data['dob'][5:7] ,'day': data['dob'][8:10]})
            print(age)
            bucket = run_model_inference([age, data["lat"], data["lng"], data["gender"], data["marital_status"], "senior software Developer"]).tolist()[0]
            data["credit_score"] = score[bucket]
            # data["bucket"] = "E3"
            data['referral_code'] = getHashedValue(data['email_id'], 6)
            # data["credit_score"] = 750
            data["bucket"] = bucket
            data["credit_amount"] = 0
            data["timestamp"] = 0

        payload = dict(data)
        m = MongoClientWrapper()
        m.write(data, 'user_test')
        # print("data value after mongo write..: ")
        # print(data)
        msg = {"status": True, "data": payload}
        # print("Payload:....")
        # print(msg)
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
        x = True
        for i in result:
            msg = {"status": True, "data": i}
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
        query = {'email_id': email}
        values = { "$set": { "total_credit": total_credit, "credit_amount": total_credit,  "timestamp": int(time.mktime(datetime.datetime.now().timetuple())) } }
        MongoClientWrapper().update(query, values, 'user_test' )
        return "True"
    elif request.method == 'GET':
        email = request.args.get("email_id")
        result = MongoClientWrapper().read({"email_id": email}, 'user_test')
        for i in result:
            limit = limit1[i["bucket"]] - int(i['credit_amount'])
            return jsonify({"limit": limit})

@app.route("/pay_dues", methods=['POST', 'GET'])
def pay_dues():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email_id']
        result = MongoClientWrapper().read({"email_id": email}, 'user_test')
        for i in result:
            credit_amount = int(i['credit_amount']) - int(data['payment'])
            if int(time.mktime(datetime.datetime.now().timetuple())) > i['timestamp'] + dueTime:
                if not i['referrerActionTaken']:
                    ref_email = i['referredBy']
                    result2 = MongoClientWrapper().read({"email_id": ref_email}, 'user_test')
                    for j in result2:
                        query = {'email_id': ref_email}
                        credit_score = j['credit_score'] - increment[j['bucket']]
                        bucket = updateBucket(credit_score)
                        values = { "$set": { "credit_score": credit_score, "bucket": bucket } }
                        MongoClientWrapper().update(query, values, 'user_test' )
                credit_score = i['credit_score'] - increment[i['bucket']]
                bucket = updateBucket(credit_score)
                query = {'email_id': email}
                values = { "$set": { "credit_score": credit_score, "bucket": bucket } }
                MongoClientWrapper().update(query, values, 'user_test' )
        return "True"
    elif request.method == 'GET':
        email = request.args.get("email_id")
        result = MongoClientWrapper().read({"email_id": email}, 'user_test')
        for i in result:
            due_amount = i['credit_amount']
            due_time = i['timestamp'] + dueTime
            return jsonify({"due_amount": due_amount, "due_time": due_time})

@app.route("/referral", methods=['POST'])
def referral():
    if request.method == 'POST':
        data = request.get_json()
        to_email = data['to_email']
        from_email = data['from_email']
        result1 = MongoClientWrapper().read({"email_id": from_email}, 'user_test')
        # result2 = MongoClientWrapper().read({"email_id": to_email}, 'user_test')
        for i in result1:
            referral_code = i['referral_code']
            data["referral_code"] = referral_code
            MongoClientWrapper().write(data,  'referral_test')
            query = {'email_id': to_email}
            values = { "$set": { "referredBy": from_email, "referrerActionTaken": False } }
            MongoClientWrapper().update(query, values, 'user_test' )
            msg = {"status": True, "text" : "Referral Sent!"}
            return jsonify(msg)
        else:
            msg = {"status": False, "text" : "Invalid Email Id Entered, Please try again"}
            return jsonify(msg)

if __name__ == "__main__":
    app.run()