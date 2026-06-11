from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Float, Integer, Text

from database.models.base import Base


class ItemModel(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, unique=False, nullable=True)
    store_id = Column(Integer, ForeignKey("store.id"), unique=False, nullable=False)
    store = relationship("StoreModel", back_populates="items")
