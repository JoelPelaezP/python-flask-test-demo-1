from flask.views import MethodView
from db import db_instance
from models import UserModel
from schemas.schemas import UserSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required
from blocklist import BLOCKLIST

blp = Blueprint("Users", "users", "User account")

@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(cls):
        return db_instance.session.query(UserModel).all()

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(cls, user_data):
        try:
            user = UserModel(
                email = user_data["email"],
                password = pbkdf2_sha256.hash(user_data["password"])
            )
            db_instance.session.add(user)
            db_instance.session.commit()
            return user
        except SQLAlchemyError:
            abort(500, 'Error ocurred internally')


@blp.route("/user/<string:email>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(cls, email):
        try:
            user = db_instance.session.query(UserModel).filter(UserModel.email == email).one_or_none()

            if user:
                return user
            
            abort(404, message="User not found.")
        except SQLAlchemyError:
            abort(500, 'Error ocurred internally')

    @blp.response(200, UserSchema)
    def delete(cls, email):
        try:
            user = db_instance.session.query(UserModel).filter(UserModel.email == email).one_or_none()
            if user:
                db_instance.session.delete(user)
                db_instance.session.commit()
                return {"message": "User deleted"}

            abort(404, message="User not found.")
        except SQLAlchemyError:
            abort(500, 'Error ocurred internally')
            

@blp.route("/user/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(cls, user_data):
        user = db_instance.session.query(UserModel).filter(UserModel.email == user_data["email"]).one_or_none()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            token = create_access_token(identity=str(user.id), fresh = True)
            reffresh_token = create_refresh_token(identity=str(user.id))
            return {"token":token, "refresh_token": reffresh_token} 
        
        abort(401)
        

@blp.route("/user/refresh")
class UserRefresh(MethodView):
    @jwt_required(fresh=True)
    def post(self):
        jti = get_jwt().get('jti')
        token = create_access_token(jti, fresh=False)
        return {"token" : token}

@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt().get('jti')
        BLOCKLIST.add(jti)

        return {"message": "successfully logout"}