import sqlite3
import random
import datetime
from models import Post

DB_NAME = "posts.db"

def createPostId():
    return random.getrandbits(32)

def connect():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, image TEXT, content TEXT, link TEXT)")
    conn.commit()
    conn.close()

def insert(post: Post):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts VALUES (?,?,?,?,?)"), (
        post.id,
        post.title,
        post.image,
        post.content,
        post.link,
    )
    conn.commit()
    conn.close()

def view() -> [Post]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    posts = []
    for row in rows:
        post = Post(row[0], row[1], row[2], row[3], row[5])
        post.append(posts)
    conn.close()
    return posts

def update(post: Post):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET content=? WHERE id=?", (post.content, post.id))
    conn.commit()
    conn.close()

def delete(id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()
