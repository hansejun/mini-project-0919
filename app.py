
from random import randint, random
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import random

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'









client = MongoClient('mongodb+srv://youwa65:ss3108@cluster0.wrjvztk.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.cafe

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/detail/<id>',methods=['GET'])
def detail(id):
    if request.method == "GET":
      return render_template('detail.html')

@app.route('/api/detail/<id>',methods=['GET'])
def get_detail(id):
  cafe = db.cafes1.find_one({'id':int(id)},{'_id':False})

  if not cafe:
    return jsonify({'success':False})
  else:
    token_exist = request.cookies.get('mytoken')
    if token_exist:
      payload = jwt.decode(token_exist, SECRET_KEY, algorithms=['HS256'])
    else:
      payload = {'id':'id'}
    reviews = list(db.review.find({'cafeId':int(id)}))
    for review in reviews:
      review["_id"] = str(review['_id'])
    doc = {
      'cafe' : cafe,
      'reviews' : reviews,
      'userId' : payload['id']
    }
  return jsonify({'success':True,'data':doc})


@app.route('/api/review',methods=['POST'])
def post_review():
  token_exist = request.cookies.get('mytoken')
  if not token_exist:
    return redirect(url_for('/login'))
  payload = jwt.decode(token_exist, SECRET_KEY, algorithms=['HS256'])
  userId = payload['id']
  cafeId = request.form['cafeId']
  comment = request.form['comment']
  rate = request.form['rate']
  createdAt = request.form['createdAt']

  doc = {
    'userId':userId,
    'cafeId' : int(cafeId),
    'comment' : comment,
    'rate' : rate,
    'createdAt' : createdAt
  }
  print(doc)
  db.review.insert_one(doc)
  return jsonify({'success':True})

@app.route('/api/review/<id>',methods=['DELETE'])
def delete_review(id):
  print(id)
  token_exist = request.cookies.get('mytoken')
  if not token_exist:
    return redirect(url_for('/login'))
  payload = jwt.decode(token_exist, SECRET_KEY, algorithms=['HS256'])
  review = db.review.find_one({'_id':ObjectId(id)})
  print(review)
  if not review:
    return jsonify({'success':False})
  if review['userId'] == payload['id']:
    db.review.delete_one({'_id':ObjectId(id)})
    return jsonify({'success':True})
  else:
    return jsonify({'success':False})
 
  

@app.route('/join')
def join():
    return render_template("join.html")

@app.route('/login')
def login():
    return render_template("login.html")




@app.route('/sign_in', methods=['POST'])
def sign_in():
    # ?????????
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # ????????? 24?????? ??????
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # ?????? ?????????
    else:
        return jsonify({'result': 'fail', 'msg': '?????????/??????????????? ???????????? ????????????.'})






@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # ?????????
        "password": password_hash,                                  # ????????????
        "profile_name": username_receive,                           # ????????? ?????? ???????????? ?????????
        "profile_pic": "",                                          # ????????? ?????? ?????? ??????
        "profile_pic_real": "profile_pics/profile_placeholder.png", # ????????? ?????? ?????? ?????????
        "profile_info": ""                                          # ????????? ??? ??????
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})









@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})








@app.route("/cafe", methods=["POST"])
def cafe_post():
    url_receive = request.form['url_give']
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    content_receive = request.form['content_give']
    doc = {
        'id' : random.randrange(1,10000),
        'content' : content_receive,
        'address' : address_receive,
        'url': url_receive,
        'name': name_receive
    }
    db.cafes1.insert_one(doc)
    return jsonify({'msg': '????????????'})
    # ???????????? ??????????????? ????????????
    # ???????????? cd
@app.route("/cafes", methods=["GET"])
def cafes_get():
    cafes = list(db.cafes1.find({}, {'_id': False}))
    return jsonify({'cafes': cafes})


if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)
