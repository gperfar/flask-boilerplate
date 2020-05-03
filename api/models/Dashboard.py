from api.core import Mixin
from .base import db
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import psycopg2, json

visualizations = db.Table('visualizations',
    db.Column('visualization_id', db.Integer, db.ForeignKey('visualization.id'), primary_key=True),
    db.Column('dashboard_id', db.Integer, db.ForeignKey('dashboard.id'), primary_key=True)
    )

class Dashboard(Mixin, db.Model):
    __tablename__ = "dashboard"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=True)
    visualizations = db.relationship('Visualization', secondary=visualizations, lazy=True,backref=db.backref('dashboards', lazy=True))

    def __init__(self, name:str, comment:str):
        self.name = name
        self.comment = comment
    def __repr__(self):
        return f"<Dashboard {self.name}>"
