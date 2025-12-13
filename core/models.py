from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlaclhemy.orm import declarative_base, relationship
from datetime import datetime 

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True)
    mrn = Column(String(50), unique=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    contact = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    reports = relationship("Report", back_populates="patient")
    predictions = relationship("Prediction", back_populates="patient")
    

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    filename = Column(String)
    file_path = Column(Text)
    uploaded_at = Column(DateTime, back_populates="reports")
    
    patient = relationship("Patient", back_populates="reports")
    
class Prediction(Base):
    __tablename__="predictions"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    malignancy = Column(String)
    probability = Column(Float)
    stage = Column(String)
    creeated_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="predictions")
    
    