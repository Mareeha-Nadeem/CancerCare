# 🚀 COMPLETE SETUP INSTRUCTIONS - Make Everything Work

## ⚠️ CURRENT ISSUE: PostgreSQL Password

Your PostgreSQL password is incorrect. Here's how to fix it:

---

## 🔧 SOLUTION 1: Find/Reset Password (Recommended)

### Option A: Remember Your Password
During PostgreSQL installation, you set a password. Try these:
- The password you wrote down
- `postgres`
- `admin`
- `root`
- `1234`
- (leave blank)

### Option B: Reset Password Using pgAdmin
1. Open **pgAdmin** (PostgreSQL GUI application)
2. Right-click on **server** → **Properties**
3. Go to **Connection** tab
4. Set new password
5. Save

### Option C: Reset via Command Line
```bash
# Open Command Prompt as Administrator
cd "C:\Program Files\PostgreSQL\16\bin"

# Connect to PostgreSQL
psql -U postgres

# If it asks for password and you don't know it, use Option D
# If it connects, run:
ALTER USER postgres WITH PASSWORD 'your_new_password';
\q
```

### Option D: Bypass Password (Temporary - For Setup Only)
1. **Find pg_hba.conf file:**
   ```
   C:\Program Files\PostgreSQL\16\data\pg_hba.conf
   ```
   (Replace 16 with your PostgreSQL version)

2. **Open as Administrator** in Notepad

3. **Find this line** (near bottom):
   ```
   host    all    all    127.0.0.1/32    scram-sha-256
   ```

4. **Change to:**
   ```
   host    all    all    127.0.0.1/32    trust
   ```

5. **Restart PostgreSQL:**
   - Windows: Services → PostgreSQL → Restart
   - Or run: `net stop postgresql-x64-16` then `net start postgresql-x64-16`

6. **Run setup (no password needed now)**

7. **IMPORTANT: Change back to `scram-sha-256` after setup for security!**

---

## 📦 STEP-BY-STEP COMPLETE SETUP

### Step 1: Install Minimal Dependencies
```bash
# Activate virtual environment
.venv\Scripts\activate

# Install core packages (avoiding problematic pandas build)
pip install streamlit sqlalchemy psycopg2-binary python-dotenv plotly

# Install pandas from wheel (pre-built, no compilation needed)
pip install --only-binary :all: pandas numpy scikit-learn

# If pandas still fails, use this:
pip install pandas --prefer-binary
```

### Step 2: Fix PostgreSQL Password
Choose ONE method from Solution 1 above and complete it.

### Step 3: Run Automatic Setup
```bash
python setup_postgres.py
```

This will:
- Guide you to enter your PostgreSQL password
- Create .env file with correct password
- Test connection
- Create database 'cancercare'
- Create all 6 tables
- Verify everything works

### Step 4: Run Application
```bash
streamlit run app.py
```

### Step 5: Open Browser
```
http://localhost:8501
```

---

## 🛠️ DEPENDENCY INSTALLATION ISSUES

### Issue: pandas fails to build
**Solution:**
```bash
# Use pre-built wheel
pip install --only-binary :all: pandas numpy

# Or specify version
pip install pandas==2.0.3 numpy==1.24.3
```

### Issue: psycopg2 fails
**Solution:**
```bash
# Use binary version (no compilation)
pip install psycopg2-binary
```

### Issue: scikit-learn fails
**Solution:**
```bash
# Use pre-built
pip install --only-binary :all: scikit-learn
```

### General Solution for All Build Errors:
```bash
# Install from minimal requirements
pip install -r requirements_minimal.txt --prefer-binary
```

---

## 📊 WHAT GETS CREATED

### Database: `cancercare`

### Tables (6 total):
1. **patients** - Patient records
   - id, mrn, name, age, gender, contact, created_at

2. **predictions** - Risk assessments
   - id, patient_id, risk_level, confidence, probabilities, created_at

3. **doctors** - Doctor information
   - id, name, email, specialization, phone, created_at

4. **appointments** - Scheduling
   - id, patient_id, doctor_id, appointment_date, reason, status, priority, notes, created_at

5. **users** - Authentication
   - id, username, email, password_hash, role, is_active, created_at, last_login

6. **reports** - Medical reports (for images!)
   - id, patient_id, filename, file_path, uploaded_at

### Configuration: `.env`
```
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/cancercare
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=dev-jwt-secret
```

---

## ✅ VERIFICATION

After setup, verify:

```bash
# Test database connection
python -c "from core.db_config import engine; engine.connect(); print('✅ Connected!')"

# Check tables
python -c "from sqlalchemy import inspect; from core.db_config import engine; print(inspect(engine).get_table_names())"
```

Should show: `['appointments', 'doctors', 'patients', 'predictions', 'reports', 'users']`

---

## 🎯 FOR IMAGE STORAGE (Your Requirement)

The `reports` table is ready for images:
- `filename` - Image filename
- `file_path` - Full path to image
- Images will be stored in: `uploads/reports/`

To add image upload feature, the backend is ready. Frontend needs:
```python
import streamlit as st

uploaded_file = st.file_uploader("Upload Cancer Scan", type=['jpg', 'png', 'dcm'])
if uploaded_file:
    # Save file
    # Create report entry with file_path
```

---

## 📞 QUICK HELP

### Can't find PostgreSQL password?
→ Use **Solution 1, Option D** (trust authentication)

### Pandas won't install?
→ Use: `pip install --only-binary :all: pandas`

### Connection refused?
→ Check PostgreSQL is running: Services → PostgreSQL

### Database exists but no tables?
→ Run: `python setup_postgres.py` again

---

## 🚀 FASTEST PATH TO WORKING PROJECT

```bash
# 1. Fix password (choose easiest for you)
Use trust authentication (Solution 1, Option D)

# 2. Install minimal packages
pip install streamlit sqlalchemy psycopg2-binary python-dotenv plotly --only-binary :all: pandas numpy

# 3. Run setup
python setup_postgres.py
# Enter any password (will work with trust mode)

# 4. Run app
streamlit run app.py
```

**Done! Project fully functional with PostgreSQL!** 🎉

---

## 📋 CHECKLIST

- [ ] PostgreSQL password fixed/bypassed
- [ ] Dependencies installed
- [ ] .env file created
- [ ] Database 'cancercare' created
- [ ] All 6 tables created
- [ ] Connection verified
- [ ] App runs without errors
- [ ] Can add patients
- [ ] Can make predictions
- [ ] Ready for image uploads

---

**Follow this guide step-by-step and everything will work!**
