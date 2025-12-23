# 🫁 CancerCare - Complete Documentation

**A comprehensive full-stack lung cancer risk prediction system integrating ML, Database Management, Computer Networks, and Data Structures & Algorithms.**

---

## 📚 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Features](#features)
4. [Installation & Setup](#installation--setup)
5. [Technology Stack](#technology-stack)
6. [Project Structure](#project-structure)
7. [DSA Implementation](#dsa-implementation)
8. [Email System](#email-system)
9. [Real-time Notifications](#real-time-notifications)
10. [ML Model](#ml-model)
11. [Database](#database)
12. [Troubleshooting](#troubleshooting)
13. [API Documentation](#api-documentation)

---

# PROJECT OVERVIEW

## ✨ Features Overview

### 🤖 AI-Powered Predictions
- Advanced ML model trained on comprehensive medical data
- Real-time risk assessment with confidence scores
- Detailed probability distributions (Low, Medium, High risk)
- Personalized recommendations

### 👥 Patient Management
- Complete CRUD operations
- Medical Record Number (MRN) tracking
- Search functionality
- Prediction history tracking
- Email notifications

### 👨‍⚕️ Doctor Portal
- Doctor registration and management
- Appointment scheduling with priority queuing
- Status tracking (scheduled, completed, cancelled)
- Statistics dashboard

### 🔍 Advanced Search (DSA-Powered)
- Linear & Binary search algorithms
- Priority queue sorting
- FIFO/LIFO ordering
- Merge sort by name/age
- Binary Search Tree for age-based queries

### 📧 Email Notifications
- Automated prediction result emails
- Appointment confirmation emails
- HTML templates with branding
- SMTP integration (Gmail/Outlook)

### 📡 Real-time Notifications
- Socket-based TCP notification server
- Broadcast messages to all clients
- Real-time appointment updates
- Network status monitoring

---

# QUICK START

## 🚀 Fastest Way to Get Started

```bash
# 1. Navigate to project
cd "e:\\Project\\CancerCare -- Copy"

# 2. Activate virtual environment
.\\.venv\\Scripts\\Activate.ps1

# 3. Run the application
streamlit run app.py
```

**Access:** http://localhost:8501

### First Steps:
1. **Add a doctor** (Doctors page → Add Doctor)
2. **Add a patient** (Patient Records → Add Patient)
3. **Make a prediction** (Single Analysis → Enter data → Analyze)
4. **Check Search** (Search page → Try DSA algorithms)

---

# FEATURES

## 🎯 Complete Feature List

### Core Features
- ✅ ML-powered lung cancer risk prediction
- ✅ Patient CRUD operations (Create, Read, Update, Delete)
- ✅ Doctor management system
- ✅ Appointment scheduling with priorities
- ✅ Advanced DSA-powered search
- ✅ Email notification system
- ✅ Real-time TCP notifications
- ✅ Dark theme UI with gradients
- ✅ Interactive charts and visualizations

### Lab Technician Features
- 📊 Single sample analysis
- 📦 Batch processing
- 📜 Patient history tracking
- 📊 Reports & export functionality
- 📅 Appointment management
- 📈 Analytics dashboard
- 🔔 Notification center
- 💬 Messaging system

### Network Features
- HTTP request/response logging
- Network performance monitoring
- JWT authentication
- Session management
- Network statistics

---

# INSTALLATION & SETUP

## 📋 Prerequisites

- **Python 3.10 or 3.11** (recommended)
- PostgreSQL 12+ or SQLite
- pip (Python package manager)
- 8GB RAM minimum
- Windows/macOS/Linux

## 🔧 Installation Steps

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/cancercare.git
cd cancercare

# Run setup script
python setup.py
```

This automatically:
- Checks Python version
- Installs dependencies
- Creates `.env` file
- Initializes database
- Seeds sample data (optional)

### Option 2: Manual Setup

**Step 1: Create Virtual Environment**
```bash
python -m venv .venv

# Windows
.\\.venv\\Scripts\\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

**Step 2: Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 3: Configure Environment**
```bash
# Copy example file
copy .env.example .env

# Edit .env with your settings
```

**Step 4: Initialize Database**
```bash
# Create database (if using PostgreSQL)
createdb cancercare

# Or use SQLite (automatic)

# Run initialization
python core/database_init.py
```

**Step 5: Run Application**
```bash
streamlit run app.py
```

---

## ⚙️ Environment Configuration

Create `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./cancercare.db
# OR for PostgreSQL:
# DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/cancercare

# Security
SECRET_KEY=your-secret-key-here-change-this
JWT_SECRET_KEY=your-jwt-secret-change-this
JWT_EXPIRATION_MINUTES=1440

# Email (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your@gmail.com
SENDER_PASSWORD=your-app-password
SENDER_NAME=CancerCare Lab

# Application
DEBUG=True
PORT=8501

# Notifications (Optional)
NOTIFICATION_SERVER_HOST=127.0.0.1
NOTIFICATION_SERVER_PORT=9999
```

---

# TECHNOLOGY STACK

## Frontend
- **Streamlit 1.29+**: Web application framework
- **Custom CSS**: Modern dark theme
- **Plotly**: Interactive visualizations
- **HTML/CSS**: Enhanced UI components
- **Font Awesome**: Professional icons (optional)

## Backend
- **Python 3.10+**: Core language
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL/SQLite**: Database
- **bcrypt**: Password hashing
- **PyJWT**: JSON Web Token authentication
- **python-dotenv**: Environment configuration

## Machine Learning
- **scikit-learn**: ML framework
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **imbalanced-learn**: SMOTE for class balancing
- **joblib**: Model persistence

## Networking
- **socket**: TCP server for notifications
- **psutil**: System monitoring
- **logging**: Application logging
- **threading**: Async operations

---

# PROJECT STRUCTURE

```
CancerCare/
├── core/
│   ├── models.py                 # Database models
│   ├── db_config.py              # Database configuration
│   ├── database_init.py          # DB initialization
│   ├── auth_manager.py           # JWT authentication
│   ├── email_service.py          # Email notifications
│   ├── icons.py                  # Icon management
│   ├── network_logger.py         # HTTP logging
│   ├── network_monitor.py        # System monitoring
│   ├── validation.py             # Input validation
│   └── services/
│       ├── patient_service.py    # Patient CRUD
│       ├── doctor_service.py     # Doctor management
│       ├── appointment_service.py # Appointments
│       ├── prediction_service.py  # ML predictions
│       └── ml_service.py         # ML model wrapper
│
├── frontend/
│   ├── home_page.py              # Landing page
│   ├── prediction_page.py        # Risk prediction
│   ├── patients_page.py          # Patient management
│   ├── doctors_page.py           # Doctor portal
│   ├── search_page.py            # DSA-powered search
│   ├── lab_dashboard.py          # Lab technician dashboard
│   ├── batch_processing.py       # Batch analysis
│   ├── patient_history.py        # Patient history
│   ├── reports_page.py           # Reports & export
│   ├── lab_tech_page.py          # Lab appointments
│   ├── dashboard_page.py         # Analytics
│   ├── notifications_page.py     # Notification center
│   ├── messaging_page.py         # Messaging
│   ├── about_page.py             # About information
│   ├── service_page.py           # Services
│   └── contact_page.py           # Contact form
│
├── data_science/
│   └── model_1/
│       ├── interface.py          # Prediction interface
│       ├── train_model.py        # Model training
│       ├── preprocess.py         # Data preprocessing
│       ├── feature_engineer.py   # Feature engineering
│       ├── data/                 # Training data
│       ├── models/               # Trained models
│       └── results/              # Model results
│
├── dsa/                          # Data Structures & Algorithms
│   ├── appointment_queue.py      # Priority queue
│   ├── bst.py                    # Binary search tree
│   ├── hashing.py                # Hash table
│   ├── patient_dsa.py            # Patient DSA (filtering, priority, BST)
│   ├── linearsearch.py           # Linear & binary search
│   ├── sorting.py                # Merge sort
│   ├── queues.py                 # Queue implementations
│   ├── stacks.py                 # Stack implementations
│   └── linked_list.py            # Linked list
│
├── database/                     # JSON data (legacy)
│   ├── patients.json
│   ├── doctors.json
│   └── appointments.json
│
├── static/                       # Static assets
│   ├── logo.png
│   └── lung.png
│
├── app.py                        # Main Streamlit application
├── config.py                     # Application configuration
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
└── README.md                     # Documentation
```

---

# DSA IMPLEMENTATION

## 🧮 Data Structures & Algorithms Usage

### **Location:** `frontend/search_page.py`
**Access:** Click "🔍 Search" in sidebar

### Implemented Algorithms

#### 1. **Linear Search** 🔍
- **File:** `dsa/linearsearch.py`
- **Complexity:** O(n)
- **Use Case:** Find patient by name/MRN/email

```python
def linear_search(arr, key, value):
    for i, item in enumerate(arr):
        if item.get(key) == value:
            return i, item
    return -1, None
```

#### 2. **Binary Search** 🎯
- **File:** `dsa/linearsearch.py`
- **Complexity:** O(log n)
- **Use Case:** Fast search on sorted data

```python
def binary_search(arr, key, value):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid].get(key)
        if mid_val == value:
            return mid, arr[mid]
        elif mid_val < value:
            low = mid + 1
        else:
            high = mid - 1
    return -1, None
```

#### 3. **Merge Sort** 📊
- **File:** `dsa/sorting.py`
- **Complexity:** O(n log n)
- **Use Case:** Sort by name/age

```python
def merge_sort(arr, key):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return _merge(left, right, key)
```

#### 4. **Priority Queue (Max-Heap)** 🚨
- **File:** `dsa/patient_dsa.py`
- **Complexity:** O(log n) per operation
- **Use Case:** Triage patients

**Priority Logic:**
1. Risk Level (HIGH > MEDIUM > LOW)
2. Age (Older first)
3. Registration date

#### 5. **FIFO Queue** ⏰
- **Complexity:** O(n log n)
- **Use Case:** Process in registration order

#### 6. **LIFO Stack** 🆕
- **Complexity:** O(n log n)
- **Use Case:** Recent patients first

#### 7. **Linear Filtering** 🎯
- **Complexity:** O(n)
- **Use Case:** Multi-criteria filtering (age, risk, name, gender)

#### 8. **Binary Search Tree** 🌳
- **Complexity:** O(log n) average
- **Use Case:** Age-range queries

```python
class AgeBST:
    def range_query(self, min_age, max_age):
        # Returns all patients in age range
        # O(log n + k) where k is result count
```

### How to Use DSA Features

1. Go to **Search** page
2. Choose algorithm:
   - **Smart Filters** → Linear filtering
   - **Direct Search** → Linear/Binary search
   - **Sort & Order** → Priority/FIFO/LIFO/Merge Sort
   - **Advanced (BST)** → Age-range BST query

---

# EMAIL SYSTEM

## 📧 Email Notification System

### Features
- **Automated prediction result emails**
- **Appointment confirmation emails**
- **Professional HTML templates**
- **SMTP integration** (Gmail, Outlook, etc.)
- **Async email delivery** (non-blocking)

### Setup

**1. Get Gmail App Password:**
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate password for "Mail"

**2. Configure `.env`:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your@gmail.com
SENDER_PASSWORD=your-app-password
SENDER_NAME=CancerCare Lab
```

**3. Add Patient Email:**
- When adding/editing patient, include email address
- System will automatically send emails for:
  - Prediction results
  - Appointment confirmations

### Email Templates

#### Prediction Result Email:
- Patient name
- Risk level (color-coded)
- Confidence score
- Probability distribution
- Recommendations
- Next steps

#### Appointment Confirmation:
- Appointment date & time
- Doctor name
- Appointment type
- Location
- Preparation instructions

### Usage

```python
from core.email_service import email_service

# Send prediction email
email_service.send_prediction_email(
    to_email='patient@example.com',
    patient_name='John Doe',
    risk_level='MEDIUM',
    confidence=0.85,
    probabilities={'LOW': 0.05, 'MEDIUM': 0.85, 'HIGH': 0.10}
)

# Send appointment email
email_service.send_appointment_email(
    to_email='patient@example.com',
    patient_name='John Doe',
    doctor_name='Dr. Smith',
    appointment_date='2025-01-15',
    appointment_time='10:00 AM'
)
```

---

# REAL-TIME NOTIFICATIONS

## 📡 TCP Notification Server

### Features
- **Socket-based TCP server**
- **Broadcast to all connected clients**
- **Real-time appointment updates**
- **Network status monitoring**
- **Auto-start on app launch**

### How It Works

1. **Server starts automatically** when app launches (port 9999)
2. **Clients connect** to receive notifications
3. **Broadcast messages** sent to all connected clients
4. **JSON-based protocol** for structured data

### Architecture

```
┌─────────────────┐
│  Streamlit App  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TCP Server     │◄──┐
│  (Port 9999)    │   │
└────────┬────────┘   │
         │            │
         ▼            │
   ┌─────────┐   ┌─────────┐
   │ Client 1│   │ Client 2│
   └─────────┘   └─────────┘
```

### Usage

```python
from core.network_logger import notification_server

# Send notification
notification_server.broadcast({
    'type': 'appointment_update',
    'message': 'New appointment scheduled',
    'data': {
        'patient_id': 123,
        'doctor_id': 456,
        'time': '2025-01-15 10:00'
    }
})
```

### Testing

```bash
# Test with telnet
telnet localhost 9999

# Or with Python client
python -c "import socket; s=socket.socket(); s.connect(('127.0.0.1', 9999)); print(s.recv(1024))"
```

---

# ML MODEL

## 🤖 Machine Learning Model

### Model Details
- **Algorithm:** Gradient Boosting Classifier
- **Features:** 15 input features
- **Output:** 3 risk classes (Low, Medium, High)
- **Training Data:** 1000+ patient records
- **Cross-Validation:** 5-fold stratified

### Training

```bash
# Navigate to model directory
cd data_science/model_1

# Run training
python train_model.py
```

**Output:**
- `models/lung_cancer_pipeline.pkl` - Trained model
- `models/model_metadata.json` - Model metadata
- `results/test_predictions.csv` - Test results

### Features Used

1. **Demographic:** AGE, GENDER
2. **Lifestyle:** SMOKING, ALCOHOL_CONSUMING
3. **Symptoms:** COUGHING, WHEEZING, CHEST_PAIN, FATIGUE, SHORTNESS_OF_BREATH, SWALLOWING_DIFFICULTY
4. **Risk Factors:** YELLOW_FINGERS, ANXIETY, PEER_PRESSURE, CHRONIC_DISEASE, ALLERGY

### Usage

```python
from core.services.ml_service import load_model

# Load model
model = load_model()

# Make prediction
features = {
    'AGE': 55,
    'SMOKING': 2,
    'YELLOW_FINGERS': 1,
    # ... other features
}

risk_level = model.predict([features])[0]
probabilities = model.predict_proba([features])[0]
```

### Model Performance
- **Accuracy:** ~85%
- **F1-Score:** ~0.84
- **Precision:** ~0.85
- **Recall:** ~0.85

---

# DATABASE

## 💾 Database Setup & Management

### Supported Databases
- **SQLite** (default, no setup required)
- **PostgreSQL** (recommended for production)

### SQLite Setup (Easy)

**Automatic** - just run the app:
```bash
streamlit run app.py
```

Database created at: `cancercare.db`

### PostgreSQL Setup

**1. Install PostgreSQL**
- Download from https://www.postgresql.org/download/
- Install and remember your password

**2. Create Database**
```sql
CREATE DATABASE cancercare;
```

**3. Update `.env`**
```env
DATABASE_URL=postgresql+psycopg2://postgres:your-password@localhost:5432/cancercare
```

**4. Initialize**
```bash
python core/database_init.py
```

### Database Schema

**Tables:**
- `patients` - Patient records
- `doctors` - Doctor information
- `appointments` - Appointment scheduling
- `predictions` - ML prediction history
- `users` - Application users
- `network_requests` - HTTP request logs
- `network_sessions` - User sessions

### Common Issues

**Issue:** "Password authentication failed"
**Fix:** Update password in `.env`

**Issue:** "Database does not exist"
**Fix:** Run `CREATE DATABASE cancercare;` in PostgreSQL

**Issue:** "Could not connect to server"
**Fix:** Make sure PostgreSQL service is running

### Database Reset

```bash
# SQLite
rm cancercare.db
python core/database_init.py

# PostgreSQL
psql -c "DROP DATABASE cancercare;"
psql -c "CREATE DATABASE cancercare;"
python core/database_init.py
```

---

# TROUBLESHOOTING

## ⚠️ Common Issues & Solutions

### Installation Issues

**Issue:** `ModuleNotFoundError: No module named 'X'`
**Fix:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Issue:** Segmentation fault when running
**Fix:** Python 3.13 not fully supported. Use Python 3.10 or 3.11
```bash
# Download Python 3.11
py -3.11 -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

### Database Issues

**Issue:** "Database connection failed"
**Fix:** Check `.env` DATABASE_URL and ensure PostgreSQL is running

**Issue:** "Table does not exist"
**Fix:**
```bash
python core/database_init.py
```

### Email Issues

**Issue:** Emails not sending
**Fix:**
1. Check SMTP credentials in `.env`
2. Enable "Less secure app access" for Gmail (or use App Password)
3. Check firewall/antivirus

### ML Model Issues

**Issue:** "Could not load ML model"
**Fix:**
```bash
cd data_science/model_1
python train_model.py
```

**Issue:** "Feature mismatch"
**Fix:** Ensure all 15 features are provided in correct order

### Performance Issues

**Issue:** App running slow
**Fix:**
- Close other applications
- Use SQLite instead of PostgreSQL
- Reduce batch size
- Clear browser cache

### Network Issues

**Issue:** Notification server won't start
**Fix:** Check if port 9999 is already in use:
```bash
# Windows
netstat -ano | findstr :9999

# Kill process if needed
taskkill /PID <PID> /F
```

---

# API DOCUMENTATION

## 📚 Service APIs

### Patient Service

```python
from core.services.patient_service import patient_service

# Create
patient, error = patient_service.create_patient({
    'mrn': 'MRN001',
    'name': 'John Doe',
    'age': 65,
    'gender': 'M',
    'contact': '555-0123',
    'email': 'john@example.com'
})

# Read
patient = patient_service.get_patient_by_mrn('MRN001')
all_patients = patient_service.get_all_patients()

# Update
patient, error = patient_service.update_patient(patient_id, {
    'contact': '555-9999'
})

# Delete
success, error = patient_service.delete_patient(patient_id)

# Search
results = patient_service.search_patients('John')
```

### Doctor Service

```python
from core.services.doctor_service import doctor_service

# Create
doctor, error = doctor_service.create_doctor({
    'name': 'Dr. Sarah Johnson',
    'specialization': 'Oncology',
    'email': 'sarah@hospital.com',
    'phone': '555-1234'
})

# Read
doctor = doctor_service.get_doctor_by_id(doctor_id)
all_doctors = doctor_service.get_all_doctors()

# Update
doctor, error = doctor_service.update_doctor(doctor_id, data)

# Delete
success, error = doctor_service.delete_doctor(doctor_id)
```

### Appointment Service

```python
from core.services.appointment_service import AppointmentService

# Create
appointment, error = AppointmentService.create_appointment({
    'patient_id': 1,
    'doctor_id': 1,
    'appointment_date': '2025-01-15',
    'appointment_time': '10:00',
    'appointment_type': 'Consultation',
    'priority': 'HIGH'
})

# Read
appointments = AppointmentService.get_appointments_by_patient(patient_id)
appointments = AppointmentService.get_appointments_by_doctor(doctor_id)

# Update
appointment, error = AppointmentService.update_appointment(appt_id, data)

# Cancel
success, error = AppointmentService.cancel_appointment(appt_id, reason)

# Delete
success, error = AppointmentService.delete_appointment(appt_id)
```

### Prediction Service

```python
from core.services.prediction_service import prediction_service

# Generate prediction
prediction, error = prediction_service.generate_prediction(
    patient_id=1,
    features={
        'AGE': 55,
        'SMOKING': 2,
        # ... other features
    }
)

# Get patient predictions
predictions = prediction_service.get_patient_predictions(patient_id)

# Get risk distribution
dist = prediction_service.get_risk_distribution()
# Returns: {'Low': 10, 'Medium': 15, 'High': 5}
```

### Email Service

```python
from core.email_service import email_service

# Send prediction email
email_service.send_prediction_email(
    to_email='patient@example.com',
    patient_name='John Doe',
    risk_level='MEDIUM',
    confidence=0.85,
    probabilities={'LOW': 0.05, 'MEDIUM': 0.85, 'HIGH': 0.10}
)

# Send appointment email
email_service.send_appointment_email(
    to_email='patient@example.com',
    patient_name='John Doe',
    doctor_name='Dr. Smith',
    appointment_date='2025-01-15',
    appointment_time='10:00 AM'
)
```

---

# SUMMARY

## 🎯 Quick Reference

### URLs
- **Main App:** http://localhost:8501
- **Notification Server:** tcp://127.0.0.1:9999

### Key Commands
```bash
# Start app
streamlit run app.py

# Initialize DB
python core/database_init.py

# Train ML model
python data_science/model_1/train_model.py

# Run setup
python setup.py
```

### Key Files
- **`.env`** - Environment configuration
- **`app.py`** - Main application
- **`requirements.txt`** - Dependencies
- **`core/database_init.py`** - DB setup
- **`data_science/model_1/train_model.py`** - ML training

### Key Features
- ✅ ML-powered predictions
- ✅ Full CRUD for patients/doctors/appointments
- ✅ DSA-powered search (8 algorithms)
- ✅ Email notifications
- ✅ Real-time TCP notifications
- ✅ Dark theme UI

### Support
- 📧 Email: support@cancercare.edu
- 🐛 Issues: GitHub Issues
- 📖 Docs: This file

---

**Built with ❤️ for academic excellence**

**Version:** 2.0  
**Last Updated:** December 2025  
**License:** MIT
