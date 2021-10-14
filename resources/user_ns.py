from flask_restplus import Namespace, Resource, abort
from flask import request, current_app
from core.models import User, Token
from core.extensions import bcrypt, db
from datetime import datetime
from sqlalchemy import exc
from core.schemas import UserSchema, UserListSchema
from marshmallow import ValidationError
from core.auth_utils import token_required
import jwt

api = Namespace('user', description='Users related operations')

@api.route('/user')
class UserResource(Resource):
    def post(self):
        user_data = request.get_json()
        if "password" in user_data:
            user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user_input_schema = UserSchema(exclude=('id', 'created_at'))
        user = User()
        try:
            user_data = user_input_schema.load(user_data, instance=user)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        user.created_at = datetime.now()
        try:
            db.session.add(user)
            db.session.commit()
        # handles errors related to database unique constraints
        except exc.IntegrityError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data": err.orig.args
            }, 400

        user_output_schema = UserSchema(exclude=['password'])
        result = user_output_schema.dump(user)

        return {
            "message": "Ok",
            "data": result
        }, 201
    
@api.route('/user/<int:user_id>')
class HandleUser(Resource):
    @token_required
    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        token_code = request.headers['Authorization']
        token = Token.query.filter_by(code=token_code).first()
        if not user or not token:
            abort(404, message="Not found")
        if not user_id == token.user_id:
            abort(401, message="Unauthorized")
        db.session.delete(user)
        db.session.commit()

        return {}, 204

    @token_required
    def put(self, user_id):
        token_code = request.headers['Authorization']
        token = Token.query.filter_by(code=token_code).first()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="Not found")
        if token.user_id != user.id:
            abort(401, message="Unauthorized")
        user_data = request.get_json()
        if "password" in user_data:
            user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user_input_schema = UserSchema(exclude=('id', 'created_at'))
        
        try:
            user_data = user_input_schema.load(user_data, instance=user, partial=True)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        try:
            db.session.commit()
        # handles errors related to database unique constraints
        except exc.IntegrityError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data": err.orig.args
            }, 400
        user_output_schema = UserSchema(exclude=['password'])
        
        # if token.user_id != user.id:
        #     user_output_schema = UserSchema(exclude=['password', 'email'])
        result = user_output_schema.dump(user)
        return {
            "message":"Ok",
            "data": result
        }, 200
    
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="Not found")
        user_output_schema = UserSchema(exclude=['password', 'email'])
        if 'Authorization' in request.headers:
            user_output_schema = UserSchema(exclude=['password'])
            token_code = request.headers['Authorization']
            try:
                jwt.decode(token_code, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                token = Token.query.filter_by(code=token_code).first()
                if not token:
                    user_output_schema = UserSchema(exclude=['password', 'email'])
                elif token.expired_at < datetime.now() or token.user_id != user_id:
                    user_output_schema = UserSchema(exclude=['password', 'email'])
            except jwt.exceptions.InvalidTokenError:
                user_output_schema = UserSchema(exclude=['password', 'email'])
        result = user_output_schema.dump(user)
        return {
            "message":"Ok",
            "data": result
        }, 200

@api.route('/users')
class UserList(Resource):
    def get(self):
        input_data = request.args
        user_list_schema = UserListSchema()
        try:
            input_data = user_list_schema.load(input_data)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        page, perPage = input_data['page'], input_data['perPage']
        if "pseudo" in input_data:
            users = User.query.filter_by(pseudo=input_data['pseudo']).order_by(User.id.desc()).paginate(page=page, per_page=perPage, error_out=False)
        else:
            users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=perPage, error_out=False)
        if not users.items and page == 1:
            return {
                "message":"Ok",
                "data":[]
            }, 200
        if page > users.pages:
            abort(400, message="Bad Request")
        user_output_schema = UserSchema(exclude=['password'])
        result = user_output_schema.dump(users.items, many=True)
        return {
            "message":"Ok",
            "data":result,
            "pager":{
                "current":page,
                "total":users.pages
            }
        }, 200