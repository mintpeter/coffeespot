from sqlalchemy import (
    Column,
    Float,
    Index,
    Integer,
    Text,
    Unicode
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

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    group = Column(Integer)

    def __init__(self, name, group):
        self.name = name
        self.group = group

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    date = Column(Float)
    title = Column(Text)
    authorid = Column(Integer)
    post = Column(Text)
    
    def __init__(self, title, authorid, post):
        self.title = title
        self.date = time.time()
        self.authorid = authorid
        self.post = post
