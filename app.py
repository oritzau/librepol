from flask import Flask, render_template, request, jsonify
import os, re, datetime
import db
from models import Post

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello"

if __name__ == "__main__":
    app.run()
