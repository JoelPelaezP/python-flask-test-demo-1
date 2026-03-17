from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from db import db_instance
from models import ItemModel
from schemas.schemas import ItemSchema, PlainItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, PlainItemSchema)
    def get(self, item_id):
        try:
            item = db_instance.session.query(ItemModel).filter(ItemModel.id == int(item_id)).one_or_none()
            if item:
                return item
        
            abort(404, message="Item not found.")
        except KeyError:
            abort(404, message="Item not found.")

    @jwt_required()
    def delete(self, item_id):
        try:
            #for testing claims in jwt, works with @jwt.additional_claims_loader
            jwt= get_jwt()
            if jwt.get("is_admin") == True:
                abort(401, message="Admin privilege required.") 

            item = db_instance.session.query(ItemModel).filter(ItemModel.id == int(item_id)).one_or_none()
            db_instance.session.delete(item)
            db_instance.session.commit()
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, PlainItemSchema)
    def put(self, item_data, item_id):
        try:
            item = db_instance.session.query(ItemModel).filter(ItemModel.id == int(item_id)).one_or_none()
            
            if item:
                item.name = item_data["name"]
            else:
                item = ItemModel(**item_data)

            db_instance.session.add(item)
            db_instance.session.commit()
            return item
        except KeyError:
            abort(404, message="Item not found.")

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, PlainItemSchema(many=True))
    def get(self):
        return db_instance.session.query(ItemModel).all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, PlainItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db_instance.session.add(item)
            db_instance.session.commit()
        except SQLAlchemyError:
            return abort(500, "Error courred internally")

        return item
