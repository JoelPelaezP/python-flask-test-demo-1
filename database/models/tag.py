# from database.config.db import db_instance

# class TagModel(db_instance.Model):
#     __tablename__ = "tag"
#     id = db_instance.Column(db_instance.Integer, primary_key=True)
#     name = db_instance.Column(db_instance.String(80), unique=True, nullable=False)

#     store_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey("store.id"))
#     store = db_instance.relationship("StoreModel", back_populates="tags")


from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.types import Integer, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database.models.base import Base

class TagModel(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)

    store_id = Column(Integer, ForeignKey("store.id"))
    store = relationship("StoreModel", back_populates="tags")