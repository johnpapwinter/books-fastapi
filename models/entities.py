from sqlalchemy import Column, Integer, String

from database import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    pages = Column(Integer)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
