from sqlalchemy import (
    Column,
    Index,
    Integer,
    Interval,
    Text
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

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    date = Column(Interval)
    title = Column(Text)
    authorid = Column(Integer)
    post = Column(Text)
    
    def __init__(self, id, title, authorid, post):
        self.id = id
        self.title = title
        self.date = time.time()
        self.authorid = authorid
        self.post = post
