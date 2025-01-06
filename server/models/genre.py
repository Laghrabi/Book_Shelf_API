from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Genre(BaseModel, Base):
    """Representation of a genre """
    __tablename__ = 'genres'
    name = Column(String(128), nullable=False)
    books = relationship("Book", back_populates="genre")

    def __init__(self, *args, **kwargs):
        """Initializes genres"""
        super().__init__(*args, **kwargs)
