"""Holds class Book"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Book(BaseModel, Base):
    """Representation of a book """
    __tablename__ = 'books'
    title = Column(String(128), nullable=False)
    genre_id = Column(String(128), ForeignKey('genres.id'))
    author = Column(String(128), nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String(512), nullable=False)
    genre = relationship("Genre", back_populates="books")
    user_books = relationship("UserBook", back_populates="book")

    def __init__(self, *args, **kwargs):
        """Initializes books"""
        super().__init__(*args, **kwargs)
