import sqlite3
import datetime
from models import Post

DB_NAME = "posts.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, image TEXT, content TEXT, link TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()
    for p in posts:
        post = Post.from_dict(p)
        insert(post)

def insert(post: Post):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (id, title, image, content, link, timestamp) VALUES (?,?,?,?,?,?)", (
        post.id,
        post.title,
        post.image,
        post.content,
        post.link,
        post.timestamp,
    ))
    conn.commit()
    conn.close()

def view() -> [Post]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    posts = []
    for row in rows:
        post = Post(row[0], row[1], row[2], row[3], row[4])
        posts.append(post)
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
    cursor.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts")
    conn.commit()
    conn.close()


posts = [
    {
        'id': 204901,
        'title': "Overflowing Sewers",
        'image': "flooded sewers",
        'content': "The sewer system is overflowing and flooding the surrounding streets in this area with dirty water. We need better systems.",
        'link': "https://en.wikipedia.org/wiki/Sewerage"
    },
    {
        'id': 204905,
        'title': "Unsafe playground",
        'image': "playground",
        'content': "Our local playground is covered in rust",
        'link': "https://en.wikipedia.org/wiki/Rust"
    },
    {
        'id': 204603,
        'title': "Inconvinient School Hours",
        'image': "N/A",
        'content': "Local middleschool ends at 3pm and there are no resources for afterschool care. I get out of work at 5pm and can't pick up my kid. Our schools need to accomodate parents who work beyond 3pm",
        'link': "N/A"
    },
    {
        'id': 204221,
        'title': "Prop 4",
        'image': "N/A",
        'content': "Allocating more funds to climate concerns could help immesurably with our wildfire problem! My house burned down in the most recent fires, we need to take action to prevent this from continuing",
        'link': "https://voterguide.sos.ca.gov/propositions/4/"
    },
    {
        'id': 204444,
        'title': "Lack of walkability",
        'image': "highway",
        'content': "There is no safe way for people without cars to get from Skidmore to walmart. The bus drops us off on the side of a busy road, which we have to cross despite the lack of sidewalks and crosswalks. I've almost been hit multiple times. We need a safer way to get there.",
        'link': "N/A"
    },
]
