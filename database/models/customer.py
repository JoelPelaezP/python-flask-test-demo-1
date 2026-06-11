from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Integer, Text

from database.models.base import Base


class CustomerModel(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    image_url = Column(Text, nullable=False)

    invoices = relationship(
        "InvoiceModel", back_populates="customer", lazy="dynamic", cascade="all, delete"
    )
