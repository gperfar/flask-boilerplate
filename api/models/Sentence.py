from api.core import Mixin
from .base import db
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import psycopg2, json
from .Connection import Connection, Postgres

# Note that we use sqlite for our tests, so you can't use Postgres Arrays
class Sentence(Mixin, db.Model):
    """Sentence Table."""
    __tablename__ = "sentence"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sql_query = db.Column(db.String, nullable=False)
    connection = db.Column(db.Integer, db.ForeignKey("connection.id", ondelete="CASCADE"), nullable=False)
    comment = db.Column(db.String, nullable=True)

    def __init__(self, name:str, sql_query:str, connection:int, comment:str):
        self.name = name
        self.sql_query = sql_query
        self.connection = connection
        self.comment = comment

    def __repr__(self):
        return f"<Sentence {self.name}>"

    def execute(self):
        connection = Connection.query.get(self.connection)
        conn = connection.start_connection()
        cur = conn.cursor()
        cur.execute(self.sql_query)
        results= cur.fetchall()
        results_json = [dict(zip([key[0] for key in cur.description], row)) for row in results] #Googleada, ni idea cómo funciona pero it does
        return results_json