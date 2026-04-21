# from database.config.db import db_instance

# class ItemModel(db_instance.Model):
#     __tablename__ = 'item'
#     id = db_instance.Column(db_instance.Integer, primary_key=True)
#     name = db_instance.Column(db_instance.String(80), unique=True, nullable=False)
#     description = db_instance.Column(db_instance.String, unique = False, nullable = True)
#     price = db_instance.Column(db_instance.Float(precision=2), unique=False, nullable=False)

#     store_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey('store.id'),  unique=False, nullable=False)
#     store = db_instance.relationship("StoreModel", back_populates='items')





from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, Text, Float
from database.models.base import Base

class ItemModel(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, unique = False, nullable = True)
    price = Column(Float(precision=2), unique=False, nullable=False)

    store_id = Column(Integer, ForeignKey('store.id'),  unique=False, nullable=False)
    store = relationship("StoreModel", back_populates='items')  