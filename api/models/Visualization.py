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
        # if(self.type == "linechart"):
            # return self.params['columns']
            # a = self.color
            # raw_dict = self.__dict__
        raw_dict.pop('_sa_instance_state', None) 
        return raw_dict
    
    def render(self):
        return "You shouldn't see this."

class VisualizationLineChart(Visualization):
    __tablename__ = "visualizationlinechart"

    id = db.Column(db.Integer, db.ForeignKey("visualization.id", ondelete="CASCADE"), primary_key=True)
    # color = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'linechart',
    }


    def __init__(self, name:str, sentence_id:int, comment:str, color:str, params:json):
        super().__init__(name=name,sentence_id= sentence_id,comment= comment, type = "linechart", params = params)
        # self.color = color
        # self.params = params

    def __repr__(self):
        return f"<Line Chart {self.name}>"
    
    def pre_render(self):
        #----------------------------------------------------------
        # Structure:                                              |
        # Column 1: X-Axis                                        |
        # Columns 2-N: Lines 1 to (N-1)                           |
        # xaxis_label: Label in X-Axis                            |
        # yaxis_label: Label in Y-Axis                            |
        # yaxis2_label: Label in secondary Y-Axis                 |
        # legend: Boolean. Whether or not to show legend          |
        #----------------------------------------------------------

        sentence = Sentence.query.get(self.sentence_id)
        results = sentence.execute()
        headers=[]
        columns=[]
        for idx, column in enumerate(self.params['columns']):
            headers.append(self.params['columns'][idx])
            temp_list = []
            for row in results:
                temp_list.append(row[headers[idx]])
            columns.append(temp_list)
        return {
            'headers':headers,
            'xaxis': columns[0],
            'lines': columns[1:],
            'xaxis_label': self.params['xaxis_label'],
            'yaxis_label': self.params['yaxis_label'],
            'yaxis2_label': self.params['yaxis2_label'] if 'yaxis2_label' in self.params else '',
            'results':results
            }
        


        return json.dumps({'a':json_result})