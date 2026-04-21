# from database.config.db import db_instance

# class StoreModel(db_instance.Model):
#     __tablename__ = 'store'
#     id = db_instance.Column(db_instance.Integer, primary_key=True)
#     name = db_instance.Column(db_instance.String(80), unique=True, nullable=False)

#     items = db_instance.relationship("ItemModel", back_populates='store', lazy='dynamic', cascade="all, delete" )
#     tags = db_instance.relationship("TagModel", back_populates="store", lazy='dynamic')



from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from database.models.base import Base

class StoreModel(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)

    items = relationship("ItemModel", back_populates='store', lazy='dynamic', cascade="all, delete" )
    tags = relationship("TagModel", back_populates="store", lazy='dynamic')
