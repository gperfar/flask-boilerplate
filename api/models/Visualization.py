from api.core import Mixin
from .base import db
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import psycopg2, json
from sqlalchemy.dialects.postgresql import JSONB
from api.models import Sentence

class Visualization(Mixin, db.Model):
    __tablename__ = "visualization"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey("sentence.id", ondelete="CASCADE"), nullable=False)
    type = db.Column(db.String, nullable=False)
    params = db.Column(db.JSON)

    __mapper_args__ = {
        'polymorphic_identity':'visualization',
        'polymorphic_on':type
    }
    def __init__(self, name:str, sentence_id:int, comment:str, type:str, params:json):
        self.name = name
        self.sentence_id = sentence_id
        self.comment = comment
        self.type = type
        self.params = params
    
    def __repr__(self):
        return f"<Visualization {self.name}>"

    def get_fields(self):
        raw_dict = self.__dict__
        raw_dict.pop('_sa_instance_state', None) 
        return raw_dict
    
    def pre_render(self):
        return "You shouldn't see this."

class VisualizationLineChart(Visualization):
    __tablename__ = "visualizationlinechart"
    id = db.Column(db.Integer, db.ForeignKey("visualization.id", ondelete="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Line chart',
    }
    def __init__(self, name:str, sentence_id:int, comment:str, params:json):
        super().__init__(name=name,sentence_id= sentence_id,comment= comment, type = "Line chart", params = params)

    def __repr__(self):
        return f"<Line Chart {self.name}>"
    
    def pre_render(self):
        sentence = Sentence.query.get(self.sentence_id)
        results = sentence.execute()
        return {
            'type': self.type,
            'column_data': self.params['columns'],
            'xaxis_label': self.params['xaxis_label'],
            'yaxis_label': self.params['yaxis_label'],
            'yaxis2_label': self.params['yaxis2_label'] if 'yaxis2_label' in self.params else '',
            'results':results
            }




class VisualizationBarChart(Visualization):
    __tablename__ = "visualizationbarchart"
    id = db.Column(db.Integer, db.ForeignKey("visualization.id", ondelete="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Bar chart',
    }
    def __init__(self, name:str, sentence_id:int, comment:str, params:json):
        super().__init__(name=name,sentence_id= sentence_id,comment= comment, type = "Bar chart", params = params)

    def __repr__(self):
        return f"<Bar Chart {self.name}>"
    
    def pre_render(self):
        sentence = Sentence.query.get(self.sentence_id)
        results = sentence.execute()
        return {
            'type': self.type,
            'column_data': self.params['columns'],
            'xaxis_label': self.params['xaxis_label'],
            'yaxis_label': self.params['yaxis_label'],
            'yaxis2_label': self.params['yaxis2_label'] if 'yaxis2_label' in self.params else '',
            'results':results
            }




class VisualizationAreaChart(Visualization):
    __tablename__ = "visualizationareachart"
    id = db.Column(db.Integer, db.ForeignKey("visualization.id", ondelete="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Area chart',
    }
    def __init__(self, name:str, sentence_id:int, comment:str, params:json):
        super().__init__(name=name,sentence_id= sentence_id,comment= comment, type = "Area chart", params = params)

    def __repr__(self):
        return f"<Area Chart {self.name}>"
    
    def pre_render(self):
        sentence = Sentence.query.get(self.sentence_id)
        results = sentence.execute()
        return {
            'type': self.type,
            'column_data': self.params['columns'],
            'xaxis_label': self.params['xaxis_label'],
            'yaxis_label': self.params['yaxis_label'],
            'yaxis2_label': self.params['yaxis2_label'] if 'yaxis2_label' in self.params else '',
            'results':results
            }