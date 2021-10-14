from flask_restplus import Namespace, Resource, abort
from flask import request, current_app
from core.models import User, Token
from core.extensions import bcrypt, db
from marshmallow import ValidationError
from core.schemas import LoginSchema, UserSchema
from datetime import datetime, timedelta
import jwt

api = Namespace('auth', description='Authentication related operations')

@api.route('/auth')
class AuthResource(Resource):
    def post(self):
        login_data = request.get_json()
        login_schema = LoginSchema()
        try:
            login_data = login_schema.load(login_data)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        
        user = User.query.filter_by(username=login_data['login']).first()
        if not user:
            abort(401, message="Unauthorized")
        if bcrypt.check_password_hash(user.password, login_data['password']):
            exp_date = datetime.now() + timedelta(hours=2)
            encoded_jwt = jwt.encode({
                "user":user.username,
                "exp":exp_date
            }, current_app.config['SECRET_KEY'], algorithm="HS256")
            user_output_schema = UserSchema(exclude=['password'])
            user_result = user_output_schema.dump(user)
            token = Token(code=encoded_jwt, expired_at=exp_date, user_id=user.id)
            db.session.add(token)
            db.session.commit()
            return {
                "message":"Ok",
                "data":{
                    "token":encoded_jwt,
                    "user":user_result
                }
            }, 201
        else:
            abort(401, message="Unauthorized")