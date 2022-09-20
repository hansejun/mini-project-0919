
from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient





client = MongoClient('mongodb+srv://youwa65:ss3108@cluster0.wrjvztk.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.cafe

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/detail/<id>',methods=['GET','POST'])
def detail():
    return render_template("detail.html")

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
