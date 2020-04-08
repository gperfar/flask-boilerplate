from api.core import Mixin
from .base import db


class User(Mixin, db.Model):
    """User Table."""
    __tablename__ = "user"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    connections = db.relationship("Connection", backref="connections")
    
    def __init__(self, name: str, email:str, password:str):
        self.name = name
        self.email = email
        self.password = password
    def __repr__(self):
        return f"<User {self.name}>"
