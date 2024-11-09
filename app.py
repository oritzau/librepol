from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import os, re
import db
from models import Post

app = Flask(__name__, static_folder='uploads')

if not os.path.isfile(db.DB_NAME):
    db.connect()


app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["ALLOWED_EXTENSIONS"] = {
    "png",
    "jpg",
    "jpeg",
    "gif",
}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowedFile(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route('/')
def index():
    base_url = request.host_url

    posts_url = f'{base_url}posts'
    response = requests.get(posts_url)
    posts = response.json()

    return render_template("display.html", posts=posts)

@app.route("/create", methods=["POST"])
def createPost():
    title = request.form.get("title")
    content = request.form.get("content")
    link = request.form.get("link")
    print(request)
    if "image" not in request.files:
        return jsonify({"status": "400", "message": "No image part"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"status": "400", "message": "No selected file"}), 400

    if file and allowedFile(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

    else:
        return jsonify({"status": "400", "message": "Invalid file format"}), 400

    post = Post(
        id=Post.createPostId(), 
        title=title,
        image=file.filename,
        content=content,
        link=link,
    )
    db.insert(post)

    return redirect("/")

@app.route("/create", methods=["GET"])
def createForm():
    return render_template("create_post.html")

@app.route("/posts", methods=["GET"])
def getRequest():
    posts = [post.serialize() for post in db.view()]
    return jsonify({
        "res": posts,
        "status": "200",
        "numposts": len(posts),
    })

@app.route('/posts/<int:id>', methods=['DELETE'])
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
