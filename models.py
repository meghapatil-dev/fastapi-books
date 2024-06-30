from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from utils import generate_sha256_hash

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String, unique=True, index=True)
    _password = mapped_column(String)
    
    reviews = relationship("Review", back_populates="user")
    
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = generate_sha256_hash(plaintext_password)

class Book(Base):
    __tablename__ = "books"
    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, index=True)
    author = mapped_column(String)
    genre = mapped_column(String)
    year_published = mapped_column(Integer)
    summary = mapped_column(Text)
    
    reviews = relationship("Review", back_populates="book")


class Review(Base):
    __tablename__ = "reviews"
    id = mapped_column(Integer, primary_key=True, index=True)
    book_id = mapped_column(Integer, ForeignKey("books.id"))
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    review_text = mapped_column(Text)
    rating = mapped_column(Integer)
    
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
