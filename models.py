"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg'

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User info'''
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.Text,
                           nullable = False)
    
    last_name = db.Column(db.Text,
                          nullable = False)
    
    image_url = db.Column(db.Text,
                          nullable = False,
                          default = DEFAULT_IMAGE)
    
    posts = db.relationship('Post', backref='user',cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        '''Return users full name for querying'''
        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    '''Blog post'''
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Text,nullable=False)
    content = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False) 


class Tag(db.Model):
    '''Tag to be added to posts'''

    __tablename__ = 'tags'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text,nullable = False, unique = True)

    posts = db.relationship('Post',secondary='posts_tags',backref='tags')


class PostTag(db.Model):
    '''Tag on post'''
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'),primary_key=True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'),primary_key=True)