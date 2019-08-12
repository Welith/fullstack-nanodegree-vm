import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string



Base = declarative_base()


''' Model representation of the user class '''
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)

    # Storing password as a hash as password should not be stored in the DB
    password_hash = Column(String(64))
    picture = Column(String(250))

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
class Category(Base):
    __tablename__ = 'category'
    name = Column(
        String(80), nullable=False
    )
    id = Column(
        Integer, primary_key=True
    )

    
    """Return object data in easily serializeable format"""
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


''' Model representation of the category_item class '''
class CategoryItem(Base):
    __tablename__ = 'category_item'
    title = Column(
        String(80), nullable=False
    )
    id = Column(
        Integer, primary_key=True
    )
    description = Column(String(250))
    price = Column(String(8))
    picture = Column(String(250))
    category_id = Column(
        Integer, ForeignKey('category.id')
    )
    category = relationship(Category)
    user_id = Column(
        Integer, ForeignKey('user.id')
    )
    user = relationship(User)

    
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


engine = create_engine('sqlite:///catalogItems.db')
Base.metadata.create_all(engine)
