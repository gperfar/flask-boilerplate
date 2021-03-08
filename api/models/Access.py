from api.core import Mixin
from .base import db
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import psycopg2, json

# Note that we use sqlite for our tests, so you can't use Postgres Arrays
class Access(Mixin, db.Model):
    """Sentence Table."""
    __tablename__ = "access"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.String, unique=False)
    model = db.Column(db.String, nullable=False)
    model_id = db.Column(db.Integer, nullable=False)
    level = db.Column(db.String, nullable=False)

    def __init__(self, user_id:str, model_id:int, model:str, level:str):
        self.user_id = user_id
        self.model = model
        self.model_id = model_id
        self.level = level 

    def __repr__(self):
        return f"<Sentence {self.name}>"
