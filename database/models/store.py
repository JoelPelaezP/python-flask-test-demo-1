from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Text

from database.models.base import Base


class StoreModel(Base):
    __tablename__ = "store"
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)

    items = relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )
    tags = relationship("TagModel", back_populates="store", lazy="dynamic")
