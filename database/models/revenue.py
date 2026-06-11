from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.types import Integer, Text

from database.models.base import Base

class RevenueModel(Base):
    __tablename__ = 'revenue'
    id = Column(Integer, primary_key=True)
    month = Column(Text, nullable=False, unique=True)
    revenue = Column(Integer, nullable=False)