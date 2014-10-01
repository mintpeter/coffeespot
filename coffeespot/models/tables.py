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

### TODO: group should be called group_id. id should be a foreign key.
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

### TODO: authorid is a foreign key. categoryid is a foreign key.
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

### TODO: id is a foreign key.
class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    def __init__(self, name):
        self.name = name
