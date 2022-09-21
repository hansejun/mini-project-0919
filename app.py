
from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient


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
  cafe = db.cafe.find_one({'id':int(id)},{'_id':False})
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
  print(request.form)
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

@app.route("/cafe", methods=["POST"])
def cafe_post():
    url_receive = request.form['url_give']
    name_receive = request.form['name_give']
    counts = list(db.cafes1.find({}, {'_id': False}))
    count = len(counts) + 1
    doc = {
        'id' : count,
        'content' : "",
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
