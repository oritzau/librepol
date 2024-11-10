from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
import os, re
import db
from models import Post
from datetime import datetime
from werkzeug.utils import secure_filename

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

app.secret_key = "very very secret"

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowedFile(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route('/')
def index():
    base_url = request.host_url

    posts_url = f'{base_url}posts'
    response = requests.get(posts_url)
    posts = response.json().get("res")

    sorted_posts = sorted(posts, key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S.%f").timestamp(), reverse=True)

    return render_template("display.html", posts=sorted_posts)

@app.route("/login", methods=["POST"])
def loginPost():
    username = request.form.get("username")
    password = request.form.get("password")
    user = db.get_moderator_by_username(username)

    if user and user.check_password(password):
        session['role'] = "moderator"
        return redirect(url_for('index'))
    return "Invalid credentials", 401

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    if session.get("role") == "moderator":
        session.pop("role", None)
    return redirect(url_for("index"))

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
        # return jsonify({"status": "400", "message": "No selected file"}), 400
        post = Post(
            id=Post.createPostId(), 
            title=title,
            image='',
            content=content,
            link=link,
            timestamp="",
        )

    elif file and allowedFile(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

    else:
        return jsonify({"status": "400", "message": "Invalid file format"}), 400

    post = Post(
        id=Post.createPostId(), 
        title=title,
        image=file.filename,
        content=content,
        link=link,
        timestamp="",
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

@app.route('/delete/', methods=['GET'])
def delete():
    if session.get('role') != "moderator":
        return redirect(url_for("login"))
    return render_template("delete_post.html")

@app.route('/delete/<int:id>', methods=['POST'])
def deletePost(id):
    if session.get('role') != "moderator":
        return redirect(url_for("login"))
    args = request.view_args
    if not args:
        return "Args not found", 404
    posts = [post.serialize() for post in db.view()]
    for post in posts:
        if post['id'] == int(args['id']):
            db.delete(post['id'])
            return redirect(url_for("index"))
    return "Post not found", 404

@app.route('/search', methods=['GET'])
def search():
    base_url = request.host_url
    posts_url = f'{base_url}posts'
    response = requests.get(posts_url)
    posts = response.json()["res"]  # Extract posts from the JSON response

    # Get the search query from the form
    query = request.args.get('query', '').lower()

    # Filter posts based on the query (searching in title and content)
    filtered_posts = [entry for entry in posts if query in entry['title'].lower() or query in entry['content'].lower()]

    sorted_posts = sorted(filtered_posts, key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S.%f").timestamp(), reverse=True)

    # Render the index template with the sorted posts
    return render_template('display.html', posts=sorted_posts)

if __name__ == "__main__":
    app.run()
