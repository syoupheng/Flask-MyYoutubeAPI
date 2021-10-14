from flask_restplus import Api
from .user_ns import api as user_api
from .auth_ns import api as auth_api
from .video_ns import api as video_api
from .comment_ns import api as comment_api

api = Api(
    title='myAPI',
    description='This is an API for handling data about users and videos',
    doc='/docs/'
    # All API metadatas
)

api.add_namespace(user_api, path='/myAPI')
api.add_namespace(auth_api, path='/myAPI')
api.add_namespace(video_api, path='/myAPI')
api.add_namespace(comment_api, path='/myAPI')