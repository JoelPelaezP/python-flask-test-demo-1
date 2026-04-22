from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Text

from database.models.base import Base


class TagModel(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)

    store_id = Column(Integer, ForeignKey("store.id"))
    store = relationship("StoreModel", back_populates="tags")
