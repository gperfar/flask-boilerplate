from api.core import Mixin
from .base import db
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import psycopg2, json

# visualizations = db.Table('visualizations',
#     db.Column('visualization_id', db.Integer, db.ForeignKey('visualization.id'), primary_key=True),
#     db.Column('dashboard_id', db.Integer, db.ForeignKey('dashboard.id'), primary_key=True)
#     )

class DashboardsVisualizations(Mixin, db.Model):
    __tablename__ = 'dashboards_visualizations'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey("dashboard.id", ondelete="CASCADE"))
    visualization_id = db.Column(db.Integer, db.ForeignKey("visualization.id", ondelete="CASCADE"))
    order = db.Column(db.Integer)
    visualization = db.relationship("Visualization", back_populates="dashboards")
    dashboard = db.relationship("Dashboard", back_populates="visualizations")


class Dashboard(Mixin, db.Model):
    __tablename__ = "dashboard"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=True)
    #visualizations = db.relationship('Visualization', secondary=visualizations, lazy=True,backref=db.backref('dashboards', lazy=True))
    visualizations = db.relationship("DashboardsVisualizations", back_populates="dashboard")

    def export(self):
        temp_vis=[]
        for vis in self.visualizations:
            temp = vis.visualization.get_fields()
            temp['order'] = vis.order
            temp_vis.append(
                # "visualization": vis.visualization.get_fields(),"order": vis.order
                temp
            )
        
        return {
            "id": self.id,
            "name": self.name,
            "comment": self.comment,
            "dashboard_visualizations": temp_vis
        }

    def __init__(self, name:str, comment:str):
        self.name = name
        self.comment = comment
    def __repr__(self):
        return f"<Dashboard {self.name}>"
