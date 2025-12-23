from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
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
    email = Column(String)  # NEW: Email field for notifications
    created_at = Column(DateTime, default=datetime.utcnow)
    
    reports = relationship("Report", back_populates="patient")
    predictions = relationship("Prediction", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
    

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    filename = Column(String)
    file_path = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="reports")
    
class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    risk_level = Column(String)  # Low, Medium, High
    confidence = Column(Float)
    probabilities = Column(Text)  # JSON string of all probabilities
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="predictions")


class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    specialization = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(DateTime, nullable=False)
    reason = Column(Text)  # Added reason field
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    priority = Column(Integer, default=1)  # 1-5, higher is more urgent
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="patient")  # patient, doctor, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)


# ========== POST-DIAGNOSIS MODELS ==========

class PostDiagnosis(Base):
    """Post-diagnosis patient information and treatment tracking"""
    __tablename__ = 'post_diagnosis'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    diagnosis_date = Column(DateTime, nullable=False)
    cancer_type = Column(String(100))  # Lung, Breast, Colon, etc.
    stage = Column(String(20))  # Stage I, II, III, IV
    tumor_size_mm = Column(Float)  # Tumor size in millimeters
    lymph_nodes_affected = Column(Integer)
    metastasis_status = Column(String(50))  # None, Regional, Distant
    treatment_plan = Column(Text)  # Detailed treatment plan
    notes = Column(Text)  # Doctor's notes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient")
    medical_images = relationship("MedicalImage", back_populates="post_diagnosis")
    tumor_markers = relationship("TumorMarker", back_populates="post_diagnosis")


class MedicalImage(Base):
    """Medical imaging storage and AI analysis results"""
    __tablename__ = 'medical_images'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    post_diagnosis_id = Column(Integer, ForeignKey('post_diagnosis.id'))
    image_type = Column(String(50))  # MRI, CT, X-Ray, PET, Ultrasound
    file_path = Column(String(500), nullable=False)  # Path to stored image
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # AI Analysis Results
    ai_analyzed = Column(Boolean, default=False)
    tumor_detected = Column(Boolean)
    confidence_score = Column(Float)  # 0.0 to 1.0
    tumor_count = Column(Integer)
    largest_tumor_size = Column(Float)  # in mm
    analysis_summary = Column(Text)  # JSON string of detailed analysis
    
    # Metadata
    image_width = Column(Integer)
    image_height = Column(Integer)
    file_size_kb = Column(Integer)
    notes = Column(Text)
    
    # Relationships
    patient = relationship("Patient")
    post_diagnosis = relationship("PostDiagnosis", back_populates="medical_images")


class TumorMarker(Base):
    """Tumor marker test results and tracking"""
    __tablename__ = 'tumor_markers'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    post_diagnosis_id = Column(Integer, ForeignKey('post_diagnosis.id'))
    
    # Marker Information
    marker_name = Column(String(50), nullable=False)  # CEA, CA19-9, CA125, PSA, AFP
    value = Column(Float, nullable=False)  # Measured value
    unit = Column(String(20))  # ng/mL, U/mL, etc.
    test_date = Column(DateTime, nullable=False)
    
    # Reference Ranges
    reference_min = Column(Float)  # Normal range minimum
    reference_max = Column(Float)  # Normal range maximum
    is_abnormal = Column(Boolean)  # True if out of reference range
    
    # Clinical Context
    lab_name = Column(String(200))  # Testing laboratory
    test_method = Column(String(100))  # Testing methodology
    notes = Column(Text)  # Doctor's interpretation
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient")
    post_diagnosis = relationship("PostDiagnosis", back_populates="tumor_markers")
