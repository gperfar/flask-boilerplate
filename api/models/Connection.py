from api.core import Mixin
from .base import db


class Connection(Mixin, db.Model):
    """Person Table."""

    __tablename__ = "connection"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    connname = db.Column(db.String, nullable=False)
    person = db.Column(db.Integer, db.ForeignKey("person.id", ondelete="SET NULL"), nullable=True)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Connection {self.name}>"
