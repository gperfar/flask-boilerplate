from api.core import Mixin
from .base import db


class Connection(Mixin, db.Model):
    __tablename__ = "connection"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=True)
    host = db.Column(db.String, nullable=True)
    database = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)
    comment = db.Column(db.String, nullable=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=True)

    def __init__(self, name: str, host:str, database:str, username:str, password:str, comment:str, user:int):
        self.name = name
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.comment = comment
        self.user = user

    def __repr__(self):
        return f"<Connection {self.name}>"
