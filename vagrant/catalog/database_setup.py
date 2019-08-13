import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
import random
import string
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

''' Model representation of the user class '''


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)

    # Storing password as a hash as password should not be stored in the DB
    password_hash = db.Column(db.String(64))
    picture = db.Column(db.String(250))

    # Encrypt the pass
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # Verify the password entered
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    """Return object data in easily serializeable format"""
    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password_hash': self.password_hash,
            'picture': self.picture
        }


''' Model representation of the category class '''


class Category(db.Model):
    __tablename__ = 'category'
    name = db.Column(
        db.String(80), nullable=False
    )
    id = db.Column(
        db.Integer, primary_key=True
    )

    """Return object data in easily serializeable format"""
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


''' Model representation of the category_item class '''


class CategoryItem(db.Model):
    __tablename__ = 'category_item'
    title = db.Column(
        db.String(80), nullable=False
    )
    id = db.Column(
        db.Integer, primary_key=True
    )
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    picture = db.Column(db.String(250))
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id')
    )
    category = db.relationship(Category)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship(User)

    """Return object data in easily serializeable format"""
    @property
    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'picture': self.picture
        }

db.create_all()