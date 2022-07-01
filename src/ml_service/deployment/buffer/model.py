from datetime import datetime


from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from ml_service.deployment.store import Base


class DataIn(Base):
    __tablename__ = "input"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


    feature_0 = Column(Float)
    feature_1 = Column(Float)
    feature_2 = Column(Float)
    feature_3 = Column(Float)
