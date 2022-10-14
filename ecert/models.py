from datetime import datetime
from ecert import db, login_manager ,app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    urole = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    def __urole__(self):
        return self.urole 


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    critere1 = db.Column(db.Integer, nullable=False)
    critere2 = db.Column(db.Integer, nullable=False)
    critere3 = db.Column(db.Integer, nullable=False)
    critere4 = db.Column(db.Integer, nullable=False)
    critere5 = db.Column(db.Integer, nullable=False)
    critere6 = db.Column(db.Integer, nullable=False)
    critere7 = db.Column(db.Integer, nullable=False)
    critere8 = db.Column(db.Integer, nullable=False)
    critere9 = db.Column(db.Integer, nullable=False)
    critere10 = db.Column(db.Integer, nullable=False)
    critere11 = db.Column(db.Integer, nullable=False)
    average = db.Column(db.Integer, nullable=False)
    opinion = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"'{self.date_posted}')"
