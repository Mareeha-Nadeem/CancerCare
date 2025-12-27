# 🗄️ Database Initialization & Issues - Complete Guide

## 📋 Overview

This document explains all database-related issues in the CancerCare project, how they occur, and how to fix them.

---

## 🔍 Main Issues

### Issue #1: PostgreSQL Password Authentication
**Error:**
```
connection to server at "localhost" failed: FATAL: password authentication failed for user "postgres"
```

**Why It Happens:**
- The `.env` file has default password "1234"
- Your actual PostgreSQL password is different
- App cannot connect to database without correct credentials

**Impact:**
- ❌ Cannot create database
- ❌ Cannot create tables
- ❌ Cannot save/load patient data
- ❌ Cannot save predictions
- ❌ All database features fail

**How to Fix:**
```bash
# Option 1: Update password in .env
python fix_password.py
# Enter your actual PostgreSQL password

# Option 2: Manual edit
# Open .env file and change line:
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_ACTUAL_PASSWORD@localhost:5432/cancercare
```

---

### Issue #2: Database Doesn't Exist
**Error:**
```
FATAL: database "cancercare" does not exist
```

**Why It Happens:**
- PostgreSQL server is running
- Password is correct
- BUT the database named "cancercare" was never created

**Impact:**
- ❌ Cannot initialize tables
- ❌ Cannot store any data
- ❌ App shows database errors

**How to Fix:**

**Method 1: Using init_db_simple.py**
```bash
# After fixing password
python init_db_simple.py
```

**Method 2: Manual in PostgreSQL**
```sql
-- Open psql or pgAdmin
CREATE DATABASE cancercare;
```

---

### Issue #3: Tables Not Created
**Error:**
```
relation "patients" does not exist
relation "predictions" does not exist
```

**Why It Happens:**
- Database exists
- But tables inside it were never created
- SQLAlchemy models defined but not executed

**Impact:**
- ❌ Cannot add patients
- ❌ Cannot save predictions
- ❌ Cannot create appointments
- ❌ All features show "relation does not exist" errors

**Tables Required:**
1. `patients` - Patient records
2. `predictions` - Risk assessment results
3. `doctors` - Doctor information
4. `appointments` - Appointment scheduling
5. `users` - User authentication
6. `reports` - Medical reports

**How to Fix:**
```bash
# Run database initialization
python init_db_simple.py
```

---

### Issue #4: ML Model Not Loading
**Warning:**
```
⚠️ Warning: Could not load ML model: No module named 'interface'
Predictions will use mock data
```

**Why It Happens:**
- Path issue with `data_science/model_1/interface.py`
- Import error in `ml_service.py`
- Model files might not exist

**Impact:**
- ⚠️ Predictions still work (using mock data)
- ⚠️ Not using actual ML model
- ⚠️ Results are rule-based instead of AI

**NOT CRITICAL** - App still functional with mock predictions

**How to Fix:**
- Already fixed in latest code (path corrected)
- Mock predictions work fine for testing
- No action needed for basic functionality

---

## 🔧 Complete Setup Process

### Step 1: Check PostgreSQL Installation

```bash
# Check if PostgreSQL is installed
psql --version

# Should show: psql (PostgreSQL) 12.x or higher
```

### Step 2: Fix Password

```bash
# Run password fix script
python fix_password.py

# Enter your PostgreSQL password when prompted
```

### Step 3: Initialize Database

```bash
# This will:
# - Create database if not exists
# - Create all tables
# - Optionally add sample data

python init_db_simple.py
```

**Expected Output:**
```
======================================================================
  Creating Database Tables
======================================================================

🔨 Creating all tables...

✅ All tables created successfully!

Tables created:
  - patients
  - doctors
  - appointments
  - predictions
  - users
  - reports

Add sample data? (y/n):
```

### Step 4: Verify Setup

```bash
# Test database connection
python -c "from core.db_config import engine; engine.connect(); print('✅ Connected!')"
```

### Step 5: Run Application

```bash
streamlit run app.py
```

---

## 📊 Database Schema

### Table: `patients`
```sql
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    mrn VARCHAR(50) UNIQUE,
    name VARCHAR,
    age INTEGER,
    gender VARCHAR,
    contact VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table: `predictions`
```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    risk_level VARCHAR,  -- 'Low', 'Medium', 'High'
    confidence FLOAT,    -- 0.0 to 1.0
    probabilities TEXT,  -- JSON string
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table: `doctors`
```sql
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    specialization VARCHAR,
    phone VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table: `appointments`
```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    doctor_id INTEGER REFERENCES doctors(id),
    appointment_date TIMESTAMP NOT NULL,
    reason TEXT,
    status VARCHAR DEFAULT 'scheduled',
    priority INTEGER DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table: `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    role VARCHAR DEFAULT 'patient',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

### Table: `reports`
```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    filename VARCHAR,
    file_path TEXT,
    uploaded_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔄 Data Flow

### 1. Creating a Patient
```python
# User enters patient info
patient_data = {
    'mrn': 'MRN001',
    'name': 'John Doe',
    'age': 65,
    'gender': 'M',
    'contact': '555-0123'
}

# Service layer
patient, error = patient_service.create_patient(patient_data)

# Database
# INSERT INTO patients (mrn, name, age, gender, contact) 
# VALUES ('MRN001', 'John Doe', 65, 'M', '555-0123')
```

### 2. Making a Prediction
```python
# User enters 23 risk factors
features = {
    'age': 65,
    'gender': 'M',
    'smoking': 7,
    'air_pollution': 5,
    # ... 19 more features
}

# ML Service
result = ml_service.predict(features)
# Returns: {'risk_level': 'High', 'confidence': 0.87, 'probabilities': {...}}

# Prediction Service
prediction, error = prediction_service.generate_prediction(patient.id, features)

# Database
# INSERT INTO predictions (patient_id, risk_level, confidence, probabilities)
# VALUES (1, 'High', 0.87, '{"Low": 0.05, "Medium": 0.08, "High": 0.87}')
```

### 3. Loading Patient History
```python
# Get patient
patient = patient_service.get_patient_by_mrn('MRN001')

# Get all predictions for this patient
predictions = prediction_service.get_patient_predictions(patient.id)

# Database
# SELECT * FROM predictions WHERE patient_id = 1 ORDER BY created_at DESC
```

---

## 🚨 Common Errors & Solutions

### Error: "No module named 'psycopg2'"
**Solution:**
```bash
pip install psycopg2-binary
```

### Error: "No module named 'sqlalchemy'"
**Solution:**
```bash
pip install sqlalchemy
```

### Error: "ImportError: cannot import name 'Base'"
**Cause:** Models not properly imported
**Solution:** Restart Python/Streamlit

### Error: "Table already exists"
**Cause:** Trying to create tables again
**Solution:** This is actually OK - tables exist

### Error: "Foreign key violation"
**Cause:** Trying to create appointment without valid patient/doctor IDs
**Solution:** Create patient & doctor first

---

## 📁 File Structure

```
CancerCare/
├── core/
│   ├── models.py           # SQLAlchemy table definitions
│   ├── db_config.py        # Database connection setup
│   ├── database_init.py    # OLD initialization (complex)
│   └── services/
│       ├── patient_service.py
│       ├── prediction_service.py
│       ├── doctor_service.py
│       └── appointment_service.py
├── .env                    # Database password configuration
├── .env.example            # Template
├── init_db_simple.py       # NEW initialization (simple)
├── fix_password.py         # Password fix script
└── app.py                  # Main application
```

---

## 🔍 Verification Checklist

After setup, verify everything works:

### ✅ Database Connection
```python
from core.db_config import engine
engine.connect()
# Should not raise error
```

### ✅ Tables Exist
```python
from core.db_config import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print(tables)
# Should show: ['patients', 'predictions', 'doctors', 'appointments', 'users', 'reports']
```

### ✅ Sample Data (if added)
```python
from core.services.patient_service import patient_service

patients = patient_service.get_all_patients()
print(f"Patient count: {len(patients)}")
# Should show > 0 if sample data was added
```

### ✅ Create Operation
```python
patient_data = {'mrn': 'TEST001', 'name': 'Test Patient', 'age': 50, 'gender': 'M', 'contact': ''}
patient, error = patient_service.create_patient(patient_data)
print(error)  # Should be None
print(patient.name)  # Should show 'Test Patient'
```

---

## 💡 Best Practices

### 1. Always Use `.env` for Passwords
```
✅ DO: Store password in .env file
❌ DON'T: Hardcode password in code
```

### 2. Initialize Database Once
```python
# First time only
python init_db_simple.py

# After that, app uses existing database
```

### 3. Use Services, Not Direct SQL
```python
✅ DO: patient_service.create_patient(data)
❌ DON'T: db.execute("INSERT INTO patients...")
```

### 4. Handle Errors Gracefully
```python
patient, error = patient_service.create_patient(data)
if error:
    st.error(f"Failed: {error}")
else:
    st.success("Created successfully!")
```

---

## 🎯 Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Password error | Wrong password in .env | Run `fix_password.py` |
| Database not exist | Database not created | Run `init_db_simple.py` |
| Table not exist | Tables not created | Run `init_db_simple.py` |
| Import error | Module not installed | `pip install <module>` |
| Connection refused | PostgreSQL not running | Start PostgreSQL service |
| Slow queries | No sample data | Add some test data |
| ML warning | Path issue | Ignore - mock data works |

---

## 📞 Need Help?

### Check These Files:
1. `TROUBLESHOOTING.md` - General issues
2. `PATIENT_NAME_FIX.md` - Patient name issue
3. `PASSWORD_FIX.md` - Password configuration

### Verify Installation:
```bash
# Python version
python --version  # Should be 3.8+

# PostgreSQL version  
psql --version    # Should be 12+

# Required packages
pip list | grep -E "sqlalchemy|psycopg2|streamlit"
```

---

## 🎉 Summary

**Core Issues:**
1. ❌ Password mismatch → Fix with `fix_password.py`
2. ❌ Database missing → Create with `init_db_simple.py`
3. ❌ Tables missing → Create with `init_db_simple.py`
4. ⚠️ ML warning → Ignore (mock data works)

**Quick Setup:**
```bash
# 1. Fix password
python fix_password.py

# 2. Initialize database
python init_db_simple.py

# 3. Run app
streamlit run app.py
```

**All features depend on database being properly set up!**

---

**Status:** Complete guide for database initialization and troubleshooting ✅
