# 🔧 Troubleshooting Guide - CancerCare

## ✅ Quick Fix for Module Errors

If you encounter `ModuleNotFoundError`, install missing packages individually:

```bash
# Essential packages (usually work without C compiler)
pip install streamlit psutil bcrypt python-jose plotly python-dotenv pyjwt
pip install sqlalchemy psycopg2-binary alembic pydantic

# If pandas/numpy/scikit-learn aren't installed, try:
pip install pandas numpy scikit-learn imbalanced-learn joblib
```

**Note:** If pandas/numpy fail due to C compiler errors, you likely already have them installed system-wide.

## Common Issues & Solutions

### 1. ModuleNotFoundError: No module named 'psutil'
**Solution:**
```bash
pip install psutil bcrypt python-jose plotly pyjwt
```

### 2. Database Connection Error
**Error:** `could not connect to server`

**Solutions:**
- Ensure PostgreSQL is running
- Check credentials in `.env` file:
  ```env
  DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/cancercare
  ```
- Create database if it doesn't exist:
  ```sql
  CREATE DATABASE cancercare;
  ```

### 3. Streamlit Port Already in Use
**Error:** `Port 8501 is already in use`

**Solutions:**
- Close other Streamlit applications
- Use a different port:
  ```bash
  streamlit run app.py --server.port=8502
  ```
- Kill the process:
  ```bash
  # Windows
  netstat -ano | findstr :8501
  taskkill /PID <PID> /F
  ```

### 4. C Compiler Not Found (pandas/numpy)
**Error:** `Unknown compiler(s): [['gcc'], ['clang']]`

**Why this happens:** Some packages need C compilation

**Solutions:**
1. **Check if already installed:**
   ```bash
   python -c "import pandas, numpy, sklearn; print('Already installed!')"
   ```

2. **Use requirements-minimal.txt:**
   ```bash
   pip install -r requirements-minimal.txt
   ```

3. **Install via Anaconda (recommended for Windows):**
   - Download Anaconda from https://www.anaconda.com/
   - Use conda to install packages:
     ```bash
     conda install pandas numpy scikit-learn
     ```

### 5. ML Model Not Loading
**Error:** Model predictions fail or show mock data

**Check:**
- Does `data_science/model_1/models/` folder exist?
- Are model files present?
- Try running the data_science scripts separately:
  ```bash
  cd data_science/model_1
  python train_model.py
  ```

### 6. Import Errors from data_science folder
**Error:** Can't import from data_science

**Solution:** The ML service automatically adds data_science to the path. If issues persist:
```bash
# Run from project root
python app.py
```

## Installation Methods

### Method 1: Quick Install (Recommended)
```bash
# Install essentials without C compiler issues
pip install streamlit psutil bcrypt python-jose plotly python-dotenv pyjwt sqlalchemy psycopg2-binary alembic pydantic

# Check if data science packages exist
python -c "import pandas, numpy, sklearn"
```

### Method 2: Full Install (if you have working pip)
```bash
pip install -r requirements-minimal.txt
```

### Method 3: Anaconda (Windows, no compiler needed)
```bash
conda install pandas numpy scikit-learn imbalanced-learn joblib
pip install streamlit psutil bcrypt python-jose plotly python-dotenv
```

## Verify Installation

Run this to check all modules:
```bash
python -c "import streamlit, psutil, bcrypt, plotly, sqlalchemy, psycopg2, pandas, numpy, sklearn; print('✅ All modules OK!')"
```

## Running the Application

### Option 1: Direct Run
```bash
streamlit run app.py
```

### Option 2: Quick Start Script
```bash
python run.py
```

### Option 3: Custom Port
```bash
streamlit run app.py --server.port=8502
```

## Database Setup

### If database doesn't exist:
```bash
# 1. Open PostgreSQL command line (psql)
# 2. Run:
CREATE DATABASE cancercare;

# Or use pgAdmin GUI to create database
```

### Initialize tables:
```bash
python core/database_init.py
```

## Testing the Setup

### 1. Test Database Connection
```bash
python -c "from core.db_config import init_database; init_database(); print('✅ Database OK!')"
```

### 2. Test ML Service
```bash
python -c "from core.services.ml_service import ml_service; print('✅ ML Service OK!')"
```

### 3. Start Application
```bash
streamlit run app.py
```

## Getting Help

1. **Check Python Version:**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **Check PostgreSQL:**
   ```bash
   psql --version  # Should be installed
   ```

3. **List Installed Packages:**
   ```bash
   pip list | grep -E "streamlit|psutil|bcrypt|pandas|sqlalchemy"
   ```

## Quick Reference

**Project runs on:** http://localhost:8501  
**Default database:** postgresql://postgres:1234@localhost:5432/cancercare  
**Required Python:** 3.8+  
**Required PostgreSQL:** 12+  

---

**Still having issues?** Check SUMMARY.md and README.md for detailed documentation.
