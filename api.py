from flask import Flask
from db_conf import db_conf
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_conf['username']}:{db_conf['password']}@{db_conf['host']}/{db_conf['db_name']}"
app.config['SECRET_KEY'] = 'dev'
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "public")
app.config["ERROR_404_HELP"] = False
# Other FLASK config varaibles ...
#app.config["ALLOWED_EXTENSIONS"] = ["jpg", "png", "mov", "mp4", "mpg"]
#app.config["MAX_CONTENT_LENGTH"] = 1000 * 1024 * 1024  # 1000mb

#app.config["MAX_CONTENT_LENGTH"] = 100 * 10 * 1

from core.extensions import db, bcrypt, ma
db.init_app(app)
bcrypt.init_app(app)
ma.init_app(app)

from resources import api
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)