from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text



class DataIn:
    __tablename__ = "input"
    created_at = Column(DateTime, default=datetime.utcnow)


    feature_0: Column(Float)
    feature_1: Column(Float)
    feature_2: Column(Float)
    feature_3: Column(Float)
