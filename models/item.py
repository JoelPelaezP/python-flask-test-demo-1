from db import db_instance

class ItemModel(db_instance.Model):
    __tablename__ = 'item'
    id = db_instance.Column(db_instance.Integer, primary_key=True)
    name = db_instance.Column(db_instance.String(80), unique=True, nullable=False)
    description = db_instance.Column(db_instance.String, unique = False, nullable = True)
    price = db_instance.Column(db_instance.Float(precision=2), unique=False, nullable=False)

    store_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey('store.id'),  unique=False, nullable=False)
    store = db_instance.relationship("StoreModel", back_populates='items')  