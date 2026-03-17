from db import db_instance

class StoreModel(db_instance.Model):
    __tablename__ = 'store'
    id = db_instance.Column(db_instance.Integer, primary_key=True)
    name = db_instance.Column(db_instance.String(80), unique=True, nullable=False)

    items = db_instance.relationship("ItemModel", back_populates='store', lazy='dynamic', cascade="all, delete" )
    tags = db_instance.relationship("TagModel", back_populates="store", lazy='dynamic')