from pyramid.security import Allow, Everyone

from sqlalchemy import (
    Column,
    Float,
    Index,
    Integer,
    Unicode,
    UnicodeText
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
    )

from zope.sqlalchemy import ZopeTransactionExtension

import time

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 0, 'admin'),
                (Allow, 0, 'edit'),
                (Allow, 1, 'edit')]
    def __init__(self, request):
        pass

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    group = Column(Integer)
    password = Column(UnicodeText)

    def __init__(self, name, group, password):
        self.name = name
        self.group = group
        self.password = password

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    date = Column(Float)
    title = Column(UnicodeText)
    authorid = Column(Integer)
    categoryid = Column(Integer)
    post = Column(UnicodeText)
    
    def __init__(self, title, authorid, categoryid, post):
        self.title = title
        self.date = time.time()
        self.authorid = authorid
        self.categoryid = categoryid
        self.post = post

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    def __init__(self, name):
        self.name = name
