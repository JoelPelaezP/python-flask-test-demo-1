from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, Integer, Text

from database.models.base import Base


class InvoiceModel(Base):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    status = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)

    customer_id = Column(
        Integer, ForeignKey("customer.id"), unique=False, nullable=False
    )
    customer = relationship("CustomerModel", back_populates="invoices")
