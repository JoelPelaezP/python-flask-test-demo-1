from db import db_instance

class TagModel(db_instance.Model):
    __tablename__ = "tag"
    id = db_instance.Column(db_instance.Integer, primary_key=True)
    name = db_instance.Column(db_instance.String(80), unique=True, nullable=False)

    store_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey("store.id"))
    store = db_instance.relationship("StoreModel", back_populates="tags")
