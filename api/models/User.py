from api.core import Mixin
from .base import db


class User(Mixin, db.Model):
    """User Table."""
    __tablename__ = "user"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    connections = db.relationship("Connection", backref="connections")
    sentences = db.relationship("Sentence", backref="sentences")
    
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Person {self.name}>"
