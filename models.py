import random
import datetime
# from werkzeug.security import generate_password_hash, check_password_hash

class Post:
    def __init__(self, id: int, title: str, image: str, content: str, link: str, timestamp):
        self.id = id
        self.title = title
        self.image = image
        self.content = content
        self.link = link
        self.timestamp=timestamp

    def __repr__(self):
        return f"<Post {self.id}>"

    def serialize(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "image" : self.image,
            "content" : self.content,
            "link" : self.link,
            "timestamp" : self.timestamp,
        }
    
    def from_dict(data: dict):
        post = Post(
            id=Post.createPostId(), 
            title=data["title"],
            image=data["image"],
            content=data["content"],
            link=data["link"],
        )
        return post

    def createPostId():
        return random.getrandbits(32)

class Moderator:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User: {self.username}>"

    def from_dict(data):
        return Moderator(
                username=data['username'],
                password=data['password'],
            )

    def serialize(self):
        return {
            'username': self.username,
        }
