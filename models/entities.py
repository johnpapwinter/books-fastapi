from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    author = Column(String)
    year = Column(Integer)
    pages = Column(Integer)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship("Genre", back_populates="books")


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    books = relationship('Book', back_populates='genre')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
