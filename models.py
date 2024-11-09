import random

class Post:
    def __init__(self, id, title, image, content, link):
        self.id = id
        self.title = title
        self.image = image
        self.content = content
        self.link = link

    def __repr__(self):
        return f"Post {self.id}"

    def serialize(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "image" : self.image,
            "content" : self.content,
            "link" : self.link,
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
