from api.core import Mixin
from .base import db
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import psycopg2, json

class Visualization(Mixin, db.Model):
    __tablename__ = "visualization"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey("sentence.id", ondelete="CASCADE"), nullable=False)
    type = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'visualization',
        'polymorphic_on':type
    }
    def __init__(self, name:str, sentence_id:int, comment:str, type:str):
        self.name = name
        self.sentence_id = sentence_id
        self.comment = comment
        self.type = type
    def __repr__(self):
        return f"<Visualization {self.name}>"

class VisualizationLineChart(Visualization):
    __tablename__ = "visualizationlinechart"

    id = db.Column(db.Integer, db.ForeignKey("visualization.id", ondelete="CASCADE"), primary_key=True)
    color = db.Column(db.String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity':'linechart',
    }


    def __init__(self, name:str, sentence_id:int, comment:str, color:str):
        super().__init__(name=name,sentence_id= sentence_id,comment= comment, type = "linechart")
        self.color = color

    def __repr__(self):
        return f"<Line Chart {self.name}>"
    