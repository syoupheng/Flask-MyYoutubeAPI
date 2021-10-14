from core.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(45), nullable=False, unique=True)
    pseudo = db.Column(db.String(45), nullable=True)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    token = db.relationship('Token', backref='user', cascade="all, delete", lazy=True)
    #video = db.relationship('Video', backref='user', cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"<User(username='{self.username}')>"

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(45), nullable=False, unique=True)
    expired_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<Token(id='{self.id}')>"

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    source = db.Column(db.String(360), nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    view = db.Column(db.Integer, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)
    #user = db.relationship('User', backref='video', cascade="all, delete", lazy=True)
    user = db.relationship('User', backref='video', lazy=True)
    video_formats = db.relationship('VideoFormat', backref='video', cascade="all, delete", lazy=True)
    comments = db.relationship('Comment', backref='video', cascade="all, delete", lazy=True)

class VideoFormat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(45), nullable=False)
    uri = db.Column(db.String(360), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id', ondelete="CASCADE"), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', backref='comments', lazy=True)
