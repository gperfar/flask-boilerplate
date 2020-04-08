from api.core import Mixin
from .base import db

# Note that we use sqlite for our tests, so you can't use Postgres Arrays
class Sentence(Mixin, db.Model):
    """Sentence Table."""
    __tablename__ = "sentence"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    sentence = db.Column(db.String, nullable=False)
    connection = db.Column(db.Integer, db.ForeignKey("connection.id", ondelete="CASCADE"), nullable=False)
    comment = db.Column(db.String, nullable=True)

    def __init__(self, sentence:str, connection:int, comment:str  ):
        self.sentence = sentence
        self.connection = connection
        self.comment = comment

    def __repr__(self):
        return f"<Sentence {self.sentence}>"
