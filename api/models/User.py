from api.core import Mixin
from .base import db
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import psycopg2, json

class User(Mixin, db.Model):
    """User Table."""
    __tablename__ = "user"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    connections = db.relationship('Connection', backref='user', lazy=True)

    def __init__(self, name: str, email:str, password:str):
        self.name = name
        self.email = email
        self.password = password
    def __repr__(self):
        return f"<User {self.name}>"

    def match_password(self, password: str):
        if (password == self.password):
            return True
        return False
