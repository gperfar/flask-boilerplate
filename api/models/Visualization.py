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
    dashboards = db.relationship("DashboardsVisualizations", back_populates="visualization")
    
    def __init__(self, name:str, sentence_id:int, comment:str, type:str, params:json):
        self.name = name
        self.sentence_id = sentence_id
        self.comment = comment
        self.type = type
        self.params = params
    
    def __repr__(self):
        return f"<Visualization {self.name}>"

    def get_fields(self):
        # raw_dict = self.__dict__
        # raw_dict.pop('_sa_instance_state', None) 
        # return raw_dict
        return {
            "name": self.name,
            "comment": self.comment,
            "sentence_id": self.sentence_id,
            "type": self.type,
            "params": self.params
        }

    def pre_render(self):
        if self.type in ["Area chart", "Bar chart", "Line chart", "Area/Bar/Line chart","Radar chart", "Pie chart", "Radial bar chart", "Scatter chart"]:
            try:
                sentence = Sentence.query.get(self.sentence_id)
                results = sentence.execute()
                return {
                    'type': self.type,
                    'column_data': self.params['columns'],
                    'xaxis_label': self.params['xaxis_label'] if 'xaxis_label' in self.params else '',
                    'yaxis_label': self.params['yaxis_label'] if 'yaxis_label' in self.params else '',
                    'yaxis2_label': self.params['yaxis2_label'] if 'yaxis2_label' in self.params else '',
                    'results':results
                    }
            except(Exception) as error:
                create_response(status=500,message= error)
        return "You shouldn't see this."


    # def export(self):
    #             return {
    #                 'type': self.type,
    #                 'column_data': self.params['columns'],
    #                 'xaxis_label': self.params['xaxis_label'] if 'xaxis_label' in self.params else '',
    #                 'yaxis_label': self.params['yaxis_label'] if 'yaxis_label' in self.params else '',
    #                 'yaxis2_label': self.params['yaxis2_label'] if 'yaxis2_label' in self.params else '',
    #                 'results':results
    #                 }
    #         except(Exception) as error:
    #             create_response(status=500,message= error)
    #     return "You shouldn't see this."
