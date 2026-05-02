from sqlalchemy import Column, Integer, String
from db import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    component = Column(String)
    status = Column(String, default="OPEN")
    rca = Column(String, nullable=True)
    severity = Column(String, default="P2")
from sqlalchemy import DateTime
import datetime

created_at = Column(DateTime, default=datetime.datetime.utcnow)
closed_at = Column(DateTime, nullable=True)    