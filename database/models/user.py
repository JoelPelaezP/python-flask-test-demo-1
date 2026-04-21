# from database.config.db import db_instance

# class UserModel(db_instance.Model):
#     __tablename__ = "user"
#     id = db_instance.Column(db_instance.Integer, primary_key=True)
#     email = db_instance.Column(db_instance.String(80), unique=True, nullable=False)
#     password = db_instance.Column(db_instance.String(1000), unique=True, nullable=False) 
#     enabled = db_instance.Column(db_instance.Boolean, nullable=True, default=False)
#     validated = db_instance.Column(db_instance.Boolean, nullable=True, default=False)


from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.types import Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from database.models.base import Base

class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, unique=True, nullable=False) 
    enabled = Column(Boolean, nullable=True, default=False)