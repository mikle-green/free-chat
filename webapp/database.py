# Database settings and models

from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db_username = "**********"
db_password = "**********"
db_hostname = "mysql.service.com"
db_name = "mysite"
db_uri = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}/{db_name}"
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    last_login = db.Column(db.DateTime(), default=datetime.utcnow)
    messages = db.relationship("Message", backref="user")

    def set_password(self, password):
	    self.password = generate_password_hash(password)

    def check_password(self, password):
	    return check_password_hash(self.password, password)

    def get_id(self):
        return self.name


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    posted_at = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
