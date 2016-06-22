from sqlalchemy import Table, Column, Integer, Text, create_engine, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship

from pyramid.security import (
Allow,
Everyone,
)

engine = create_engine('sqlite:///divinity.db')
Session = sessionmaker()
Base = declarative_base(bind=engine)

first_item_table = Table('first_items_a', Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('recipe_id', Integer, ForeignKey('recipes.id'))
)
second_item_table = Table('second_items_a', Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('recipe_id', Integer, ForeignKey('recipes.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    fullname = Column(String, nullable = True)
    info = Column(Text, nullable = True)    

    def __repr__(self):
        return self.name + " " + self.password + " "

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    image = Column(String)
    name = Column(String)
    info = Column(Text, nullable = True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', backref = backref('items', lazy='dynamic'))
    first_items = relationship("Recipe", secondary=first_item_table, back_populates="first_item")
    second_items = relationship("Recipe", secondary=second_item_table, back_populates="second_item")
    
class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    level = Column(String)
    result_item_id = Column(Integer, ForeignKey('items.id'))
    result_item = relationship('Item', backref = backref('recipe_use', lazy='dynamic'))
    first_item = relationship("Item", secondary=first_item_table, back_populates="first_items")
    second_item = relationship("Item", secondary=second_item_table, back_populates="second_items")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class AccessGroups(object):
    	__name__ = None
	__acl__ = [
	(Allow, 'group:editors', 'edit'),       
	(Allow, Everyone, 'view'),
	    ]
	def __init__(self, request):
        	pass
