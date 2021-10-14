from core.extensions import ma
from core.models import User, Video
from marshmallow import fields, validate

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
    id = ma.auto_field()
    username = ma.auto_field(validate=[validate.Length(min=1, max=45), validate.Regexp("^[a-zA-Z0-9_-]*$")])
    email = ma.auto_field(validate=[validate.Length(max=45), validate.Email()])
    pseudo = ma.auto_field(validate=validate.Length(min=1, max=45))
    password = ma.auto_field(validate=validate.Length(min=8))
    created_at = ma.auto_field()
    # id = fields.Int()
    # username = fields.Str(required=True, validate=[validate.Length(min=1, max=45), validate.Regexp("^[a-zA-Z0-9_-]*$")])
    # email = fields.Email(required=True, validate=validate.Length(max=45))
    # pseudo = fields.Str(validate=validate.Length(min=1, max=45))
    # password = fields.Str(required=True, validate=validate.Length(min=8))
    # created_at = fields.DateTime()

class LoginSchema(ma.Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)

class UserListSchema(ma.Schema):
    pseudo = fields.Str(required=False, validate=validate.Length(min=1, max=45))
    page = fields.Int(required=False, missing=1, validate=validate.Range(min=1))
    perPage = fields.Int(required=False, missing=5,validate=validate.Range(min=1))

class VideoSchema(ma.Schema):
    name=fields.Str(required=False, validate=validate.Length(min=1, max=45))
    source=fields.Str(required=True, validate=validate.Length(max=360))
    id = fields.Int()
    user_id = fields.Int()
    created_at = fields.DateTime()
    view = fields.Int()
    enabled = fields.Int()
    user = fields.Nested(UserSchema(exclude=['password', 'email']))

class VideoListSchema(ma.Schema):
    name = fields.Str(required=False, validate=validate.Length(min=1, max=45))
    user = fields.Int(required=False)
    duration = fields.Int(required=False, validate=validate.Range(min=1))
    page = fields.Int(required=False, missing=1, validate=validate.Range(min=1))
    perPage = fields.Int(required=False, missing=5,validate=validate.Range(min=1))

class VideoPatchSchema(ma.Schema):
    format = fields.Int(required=False, validate=[validate.OneOf([1080, 720, 480, 360, 240, 144])])
    file = fields.Str(required=False, validate=validate.Length(max=360)) 

class VideoUpdateSchema(ma.Schema):
    name=fields.Str(required=False, validate=validate.Length(min=1, max=45))
    user=fields.Int()

class CommentSchema(ma.Schema):
    id = fields.Int()
    body = fields.Str(required=False)
    user = fields.Nested(UserSchema(exclude=['password', 'email']))

class CommentListSchema(ma.Schema):
    page = fields.Int(required=False, missing=1, validate=validate.Range(min=1))
    perPage = fields.Int(required=False, missing=5,validate=validate.Range(min=1))