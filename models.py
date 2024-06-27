

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True,nullable=False)
    password = db.Column(db.String(500), nullable=False)


    def __repr__(self):
        return f"<users {self.id}>"