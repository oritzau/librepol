from flask import Flask, render_template, request, jsonify
import os, re, datetime
import db
from models import Post

app = Flask(__name__)

if not os.path.isfile(db.DB_NAME):
    db.connect()

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/request", methods=["POST"])
def postRequest():
    data = request.get_json()
    post = Post(
        id=db.createPostId(), 
        title=data["title"],
        image=data["image"],
        content=data["content"],
        link=data["link"],
    )
    db.insert(post)

    return jsonify({
        "res": post.serialize(),
        "status": "200",
        "msg": "Created new post",
    })

@app.route("/request", methods=["GET"])
def getRequest():
    posts = [post.serialize() for post in db.view()]
    return jsonify({
        "res": posts,
        "status": "200",
        "numposts": len(posts),
    })

@app.route('/request/<int:id>', methods=['DELETE'])
def deleteRequest(id):
    args = request.view_args
    if not args:
        return jsonify({
            'res': '',
            'status': '404'
        })   
    posts = [post.serialize() for post in db.view()]
    for post in posts:
        if post['id'] == int(args['id']):
            db.delete(post['id'])
            posts = [post.serialize() for post in db.view()]
            print('updated_bks: ', posts)
            return jsonify({
                'res': posts,
                'status': '200',
                'numposts': len(posts)
            })
    return jsonify({
        'res': '',
        'status': '404'
    })   

if __name__ == "__main__":
    app.run()
