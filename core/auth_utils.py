from datetime import datetime
from flask_restplus import abort
from flask import request, current_app
from functools import wraps
from core.models import User, Token
import jwt

def token_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401, message="Unauthorized")
        token_code = request.headers['Authorization']
        if not token_code:
            abort(401, message="Unauthorized")
        try:
            jwt.decode(token_code, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            abort(401, message="invalid token")

        token = Token.query.filter_by(code=token_code).first()
        if not token:
            abort(401, message="Unauthorized")
        if token.expired_at < datetime.now():
            abort(401, message="expired token")
        
        
        user = User.query.filter_by(id=token.user_id).first()
        if not user:
            abort(401, message="Unauthorized")
        
        return func(*args, **kwargs)
    return wrapped