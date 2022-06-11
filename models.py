from sqlalchemy.sql import func
from sqlalchemy import DateTime
from database import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.Text(), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    register_date = db.Column(DateTime, default=func.now())#db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password

class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    create_date =  db.Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, title, author, body):
        self.title = title
        self.author = author
        self.body = body

