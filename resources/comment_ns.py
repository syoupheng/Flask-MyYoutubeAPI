from flask_restplus import Namespace, Resource, abort
from flask import request, current_app
from core.models import User, Token, Video, Comment
from core.extensions import bcrypt, db
from datetime import datetime
from sqlalchemy import exc
from core.schemas import CommentListSchema, CommentSchema, UserSchema, UserListSchema
from marshmallow import ValidationError
from core.auth_utils import token_required
import jwt

api = Namespace('comment', description='Comments related operations')

@api.route("/video/<int:video_id>/comment")
class CommentResource(Resource):
    @token_required
    def post(self, video_id):
        data = request.get_json()
        comment_input_schema = CommentSchema(only=['body'])
        try:
            comment_data = comment_input_schema.load(data)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400

        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Not found")
        token = Token.query.filter_by(code=request.headers['Authorization']).first()
        if "body" in comment_data:
            body = comment_data['body']
        else:
            body = ""
        comment = Comment(body=body, user_id = token.user_id, video_id=video_id)
        db.session.add(comment)
        db.session.commit()
        comment_output_schema = CommentSchema()
        result = comment_output_schema.dump(comment)

        return {
            "message":"Ok",
            "data":result
        }, 201

@api.route("/video/<int:video_id>/comments")
class CommentListResource(Resource):
    @token_required
    def get(self, video_id):
        data = request.args
        input_schema = CommentListSchema()
        try:
            input_data = input_schema.load(data)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        page, perPage = input_data['page'], input_data['perPage']
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Not found")
        comments = Comment.query.filter_by(video_id=video_id).order_by(Comment.id.desc()).paginate(page=page, per_page=perPage, error_out=False)
        if not comments.items and page == 1:
            return {
                "message":"Ok",
                "data":[]
            }, 200
        if page > comments.pages:
            abort(400, message="Bad Request")
        comment_output_schema = CommentSchema()
        result = comment_output_schema.dump(comments.items, many=True)

        return {
            "message":"Ok",
            "data":result,
            "pager":{
                "current":page,
                "total":comments.pages
            }
        }, 200