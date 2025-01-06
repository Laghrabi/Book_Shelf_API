from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship


class UserBook(BaseModel, Base):
    """UserBook class"""
    __tablename__ = 'user_books'
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    book_id = Column(String(128), ForeignKey('books.id'), nullable=False)
    read = Column(BOOLEAN, default=False)
    like = Column(BOOLEAN, default=False)
    user = relationship('User', back_populates='user_books')
    book = relationship('Book', back_populates='user_books')
