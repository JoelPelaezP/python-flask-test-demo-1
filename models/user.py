from db import db_instance

class UserModel(db_instance.Model):
    __tablename__ = "user"
    id = db_instance.Column(db_instance.Integer, primary_key=True)
    email = db_instance.Column(db_instance.String(80), unique=True, nullable=False)
    password = db_instance.Column(db_instance.String(80), unique=True, nullable=False) 
    enabled = db_instance.Column(db_instance.Boolean, nullable=True, default=False)
    validated = db_instance.Column(db_instance.Boolean, nullable=True, default=False)