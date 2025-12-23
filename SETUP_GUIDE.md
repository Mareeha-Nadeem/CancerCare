# 🚀 CancerCare - Complete Setup Guide

## Using Database Wizard (Easiest Method)

### Prerequisites
1. **PostgreSQL Installed** (version 12 or higher)
2. **Python 3.8+** installed
3. **PostgreSQL is running**

### Step-by-Step Setup

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Run Database Wizard
```bash
python db_wizard.py
```

#### 3. Follow Interactive Prompts

**The wizard will ask you:**

```
PostgreSQL Host (default: localhost): 
# Press Enter for localhost or type your host

PostgreSQL Port (default: 5432): 
# Press Enter for 5432 or type your port

PostgreSQL Username (default: postgres): 
# Press Enter for postgres or type your username

PostgreSQL Password: 
# Type your PostgreSQL password (hidden)

Database Name (default: cancercare): 
# Press Enter for cancercare or type custom name

Add sample data for testing? (y/n): 
# Type 'y' for sample data or 'n' to skip
```

#### 4. Wizard Automatically:
- ✅ Tests PostgreSQL connection
- ✅ Creates `cancercare` database
- ✅ Creates all 6 tables (patients, predictions, doctors, appointments, users, reports)
- ✅ Adds sample data (if you chose yes)
- ✅ Updates `.env` file with correct password
- ✅ Verifies everything works

#### 5. Run Application
```bash
streamlit run app.py
```

#### 6. Open Browser
```
http://localhost:8501
```

---

## What the Wizard Does

### Database Creation
```sql
CREATE DATABASE cancercare;
```

### Tables Created
1. **patients** - Patient records
2. **predictions** - ML risk assessments  
3. **doctors** - Doctor information
4. **appointments** - Scheduling system
5. **users** - Authentication
6. **reports** - Medical reports

### Sample Data (if selected)
- 3 Sample patients (MRN001, MRN002, MRN003)
- 2 Sample doctors (Oncologist, Pulmonologist)

### Configuration File (.env)
```
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/cancercare
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-change-this
```

---

## Troubleshooting

### Issue: "Connection failed"
**Fix:**
1. Make sure PostgreSQL is running
2. Check username/password are correct
3. Verify PostgreSQL is on port 5432

### Issue: "Permission denied"
**Fix:**
Run as administrator or ensure PostgreSQL user has CREATE DATABASE permission

### Issue: "Module not found"
**Fix:**
```bash
pip install sqlalchemy psycopg2-binary python-dotenv
```

---

## Verification

After setup, verify everything:

### Check Database
```bash
# Windows
psql -U postgres -d cancercare -c "\\dt"

# Should show all 6 tables
```

### Check Application
```bash
streamlit run app.py
```

Navigate to:
- 🔬 Lab Dashboard - Should load without errors
- 👥 Patient Records - Should show sample patients (if added)

---

## Alternative Methods

### Method 1: Manual Setup (Old Way)
```bash
# 1. Fix password
python fix_password.py

# 2. Initialize database
python init_db_simple.py

# 3. Run app
streamlit run app.py
```

### Method 2: Using psql
```bash
# 1. Create database
psql -U postgres
CREATE DATABASE cancercare;
\\q

# 2. Create tables
python
>>> from core.models import Base
>>> from core.db_config import engine
>>> Base.metadata.create_all(engine)
>>> exit()

# 3. Run app
streamlit run app.py
```

---

## Complete Feature List

After setup, you'll have access to:

### Lab Technician Features
- 🔬 Lab Dashboard (Today's overview)
- 🧪 Single Sample Analysis (23 risk factors)
- 📦 Batch Processing (CSV upload)
- 📜 Patient History (Timeline & trends)
- 📊 Reports & Export (Multiple formats)
- 📅 Appointment Scheduling

### Data Management
- 👥 Patient Records
- 👨‍⚕️ Doctor Management
- 📈 Analytics Dashboard

### Communication
- 🔔 Live Notifications
- 💬 Real-time Messaging

---

## Quick Reference

### Start Application
```bash
streamlit run app.py
```

### Re-run Wizard (Reset Database)
```bash
python db_wizard.py
```

### Check Database Status
```bash
python -c "from core.db_config import engine; engine.connect(); print('✅ Connected!')"
```

### Add More Sample Data
```python
python
>>> from core.services.patient_service import patient_service
>>> patient_service.create_patient({'mrn': 'MRN004', 'name': 'Test', 'age': 50, 'gender': 'M', 'contact': ''})
```

---

## Configuration Files

### .env (Created by Wizard)
```
DATABASE_URL=postgresql+psycopg2://USER:PASS@HOST:PORT/DB
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

### requirements.txt
All needed packages are already listed

---

## Support

### Documentation
- `DATABASE_ISSUES_EXPLAINED.md` - Database troubleshooting
- `FINAL_FEATURES.md` - Complete feature guide
- `README_LAB_TECH.md` - Lab technician guide
- `PATIENT_NAME_FIX.md` - Patient name fix

### Common Commands
```bash
# Reinstall packages
pip install -r requirements.txt

# Reset database (run wizard again)
python db_wizard.py

# Check PostgreSQL status
# Windows: Services → PostgreSQL
# Mac/Linux: sudo service postgresql status
```

---

## Success Indicators

After running wizard, you should see:

```
✅ Setup Complete!

Database Configuration:
  Host:     localhost
  Port:     5432
  Database: cancercare
  Username: postgres

📁 Configuration saved to: .env

🚀 Next Steps:
  1. Run the application:
     streamlit run app.py
```

Then when you run the app:
- ✅ No database errors
- ✅ Navigation appears
- ✅ Lab Dashboard loads
- ✅ Can add patients
- ✅ Can make predictions

---

**You're all set! The project is now fully functional.** 🎉
