from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.types import Boolean, Integer, Text

from database.models.base import Base


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, unique=True, nullable=False)
    enabled = Column(Boolean, nullable=True, default=False)
    validated = Column(Boolean, nullable=True, default=False)
    is_admin = Column(Boolean, nullable=True, default=False)
