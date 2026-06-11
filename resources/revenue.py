from flask.views import MethodView
from flask_smorest import Blueprint

import app
from database.models import RevenueModel
from schemas.schemas import RevenueSchema

blp = Blueprint("Revenues", "revenues", "Revenue Models")


@blp.route("/revenue")
class RevenueList(MethodView):
    @blp.response(200, RevenueSchema(many=True))
    def get(cls):
        with app.db_session() as db_session:
            return db_session.query(RevenueModel)
