from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'








#client = MongoClient('mongodb+srv://test:sparta@cluster0.l5fmn4e.mongodb.net/Cluster0?retryWrites=true&w=majority')
#db = client.popular


client = MongoClient('mongodb+srv://youwa65:ss3108@cluster0.wrjvztk.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.cafe

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")

# /detail/<id>
# def detail(id)
@app.route('/detail/<id>',methods=['GET'])
def detail(id):
    if request.method == "GET":
      return render_template('detail.html')

@app.route('/api/detail/<id>',methods=['GET'])
def get_detail(id):
  # 받아온 카페 id를 가지고 있는 카페 데이터를 찾는다.
  cafe = db.cafes1.find_one({'id':int(id)},{'_id':False})
  # 없으면 실패 리턴
  if not cafe:
    return jsonify({'success':False})
  # 있으면 ~~
  else:
    # review DB에서 받아온 카페 아이디를 가지고 있는 모든 review 데이터들을 가져온다.
    reviews = list(db.review.find({'cafeId':int(id)}))
    # ObjectId를 String 형식으로 바꿔준다.
    for review in reviews:
      review["_id"] = str(review['_id'])
    # front에 {sucess:true, data:{cafe:해당 카페 데이터, 해당 카페에 대한 리뷰들 }}을 전달한다.
    doc = {
      'cafe' : cafe,
      'reviews' : reviews
    }
  return jsonify({'success':True,'data':doc})


@app.route('/api/review',methods=['POST'])
def post_review():
  # token 확인
  # token에서 userId 추출
  # userId = user.id
  userId = "qwer123"
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

  db.review.insert_one(doc)
  return jsonify({'success':True})

@app.route('/api/review/<id>',methods=['DELETE'])
def delete_review(id):
  # token 확인 
  # token에서 userId 추출
  # review = db.review.find_one({'_id':ObjectId(id)}) // 받아온 카페의 아이디를 가지고 있는 review 데이터가 있는지 확인
  # review가 없다면 success false 반환 
  # review가 있다면 review['userId']와 토큰에서 가져온 userId가 같은지 확인 
  # 일치하다면 삭제
  return jsonify({'success':True})

@app.route('/join')
def join():
    return render_template("join.html")

@app.route('/login')
def login():
    return render_template("login.html")




@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})






@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
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
    counts = list(db.cafes1.find({}, {'_id': False}))
    count = len(counts) + 1
    doc = {
        'id' : count,
        'content' : content_receive,
        'address' : address_receive,
        'url': url_receive,
        'name': name_receive
    }
    db.cafes1.insert_one(doc)
    return jsonify({'msg': '저장완료'})

@app.route("/cafes", methods=["GET"])
def cafes_get():
    cafes = list(db.cafes1.find({}, {'_id': False}))
    return jsonify({'cafes': cafes})


if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)
