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
    user_id = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    sentences = db.relationship('Sentence', backref='connection', lazy=True,cascade="all, delete-orphan")

    def __init__(self, name: str, comment:str, user_id:str, type:str):
        self.name = name
        self.comment = comment
        self.user_id = user_id
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
            # raw_dict.pop('password', None) 
            raw_dict.pop('id', None) 
            raw_dict.pop('user_id', None) 

            return raw_dict           



class Postgres(Connection):
    __tablename__ = "postgres"

    id = db.Column(db.Integer, db.ForeignKey("connection.id", ondelete="CASCADE"), primary_key=True)
    host = db.Column(db.String, nullable=False)
    database = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False)

    def __init__(self, name: str, host:str, database:str, username:str, password:str, comment:str, user_id:str, port:int):
        super().__init__(name=name,user_id= user_id,comment= comment, type = "postgres")
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port

    def __repr__(self):
        return f"<Connection {self.name}>"
    
    def start_connection(self):
        conn = None
        #Connect to the DB	
        conn = psycopg2.connect(
            host = self.host,
            database = self.database, 
            user = self.username, 
            password = self.password,
            port=self.port)
        return conn