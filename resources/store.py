from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

import app
import utility.logger
from database.models import StoreModel
from external_services.weather.factory import create_client
from schemas.schemas import PlainStoreSchema, StoreSchema

logger = utility.logger.get_logger(__name__)
blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        try:
            with app.db_session() as db_session:
                store = (
                    db_session.query(StoreModel)
                    .filter(StoreModel.id == int(store_id))
                    .one_or_none()
                )
                if store:
                    return store

            abort(404, message="Store not found.")
        except:
            abort(404, message="Store not found.")

    def delete(cls, store_id):
        try:
            with app.db_session() as db_session:
                store = (
                    db_session.query(StoreModel)
                    .filter(StoreModel.id == int(store_id))
                    .one_or_none()
                )
                db_session.delete(store)
                return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")

    @blp.arguments(PlainStoreSchema)
    @blp.response(201, StoreSchema)
    def put(cls, store_data, store_id):
        try:
            with app.db_session() as db_session:
                store = (
                    db_session.query(StoreModel)
                    .filter(StoreModel.id == int(store_id))
                    .one_or_none()
                )

                if store:
                    store.name = store_data["name"]
                else:
                    store = StoreModel(**store_data)

                db_session.add(store)
                return store
        except SQLAlchemyError:
            abort(500, "Error ocurred internally")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        client = create_client()

        response = client.get_data()

        logger.info("Weather API Response")

        with app.db_session() as db_session:
            return db_session.query(StoreModel).all()

    @blp.arguments(PlainStoreSchema)
    @blp.response(201, StoreSchema)
    def post(cls, store_data):
        store = StoreModel(**store_data)

        try:
            with app.db_session() as db_session:
                db_session.add(store)
        except SQLAlchemyError:
            abort(500, "Error ocurred internally")
        return store
