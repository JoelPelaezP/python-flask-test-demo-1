import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.schemas import PlainStoreSchema, StoreSchema
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError
from db import db_instance


blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        try:
            store = db_instance.session.query(StoreModel).filter(StoreModel.id == int(store_id)).one_or_none()
            if store:
                return store
            
            abort(404, message="Store not found.")
        except:
            abort(404, message="Store not found.")

    def delete(cls, store_id):
        try:
            store = db_instance.session.query(StoreModel).filter(StoreModel.id == int(store_id)).one_or_none()
            db_instance.session.delete(store)
            db_instance.session.commit()
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")
            
    @blp.arguments(PlainStoreSchema)
    @blp.response(201, StoreSchema)
    def put(cls, store_data, store_id):
        try:
            store = db_instance.session.query(StoreModel).filter(StoreModel.id == int(store_id)).one_or_none()

            if store:
                store.name = store_data["name"]
            else:
                store = StoreModel(**store_data)

            db_instance.session.add(store)
            db_instance.session.commit()
            return store
        except SQLAlchemyError:
            abort(500, "Error ocurred internally")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return db_instance.session.query(StoreModel).all()

    @blp.arguments(PlainStoreSchema)
    @blp.response(201, StoreSchema)
    def post(cls, store_data):
        store = StoreModel(**store_data)

        try:
            db_instance.session.add(store)
            db_instance.session.commit()
        except SQLAlchemyError:
            abort(500, 'Error ocurred internally')
        return store
