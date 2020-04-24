from api.core import Mixin
from .base import db
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import psycopg2, json

class Connection(Mixin, db.Model):
    __tablename__ = "connection"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    type = db.Column(db.String, nullable=False)

    def __init__(self, name: str, comment:str, user:int, type:str):
        self.name = name
        self.comment = comment
        self.user = user
        self.type = type

    def __repr__(self):
        return f"<Connection {self.name}>"

    def start_connection(self):
        if(self.type == "postgres"):
            return Postgres.query.get(self.id).start_connection()

    def get_fields(self):
        if(self.type == "postgres"):
            raw_dict = Postgres.query.get(self.id).__dict__
            raw_dict.pop('_sa_instance_state', None) 
            return raw_dict           



class Postgres(Connection):
    __tablename__ = "postgres"

    id = db.Column(db.Integer, db.ForeignKey("connection.id", ondelete="CASCADE"), primary_key=True)
    host = db.Column(db.String, nullable=False)
    database = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, name: str, host:str, database:str, username:str, password:str, comment:str, user:int):
        super().__init__(name=name,user= user,comment= comment, type = "postgres")
        self.host = host
        self.database = database
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<Connection {self.name}>"
    
    def start_connection(self):
        conn = None
        #Connect to the DB	
        conn = psycopg2.connect(
            host = self.host,
            database = self.database, 
            user = self.username, 
            password = self.password)
        return conn