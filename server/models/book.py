"""Holds class Book"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer


class User(BaseModel, Base):
    """Representation of a book """
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    author = Column(String(128), nullable=False)
    genre = Column(String(128), nullable=False)
    year = Column(Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)