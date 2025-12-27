# 🚀 CancerCare Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.8 or higher installed
- [ ] PostgreSQL installed and running
- [ ] Database `cancercare` created in PostgreSQL

## Setup Database (If not done)

```sql
-- Open PostgreSQL terminal (psql)
CREATE DATABASE cancercare;
```

Or use pgAdmin to create the database.

## Installation Commands

```bash
# Navigate to project directory
cd "e:\Project\CancerCare -- Copy"

# Run setup (recommended)
python setup.py

# OR install dependencies manually
pip install -r requirements.txt

# Initialize database
python core/database_init.py
```

## Running the Application

```bash
# Quick start
python run.py

# OR manually
streamlit run app.py
```

The application will open at: **http://localhost:8501**

## First Time Usage

### Step 1: Explore Home Page
- View features and information
- Understand the project scope

### Step 2: Add a Doctor (Optional)
1. Click "Doctors Portal" or navigate via sidebar
2. Go to "Add Doctor" tab
3. Fill in doctor information
4. Click "Register Doctor"

### Step 3: Add a Patient (Optional)
1. Click "View Patients" or use sidebar
2. Go to "Add Patient" tab
3. Enter patient details (MRN, name, age, etc.)
4. Click "Add Patient"

### Step 4: Make a Prediction
1. Click "Start Prediction" or navigate to Prediction page
2. Fill in patient information:
   - Age, Gender, MRN (optional)
   - Risk factors (smoking, pollution, etc.)
   - Medical history
   - Symptoms
3. Click "Predict Risk Level"
4. View results:
   - Risk level (Low/Medium/High)
   - Confidence score
   - Probability chart
   - Recommendations

### Step 5: View Network Statistics
1. Go to "Doctors Portal"
2. Click "Network Stats" tab
3. View:
   - Request/response statistics
   - System metrics
   - Network performance

## Troubleshooting

### Database Connection Error
```
Error: could not connect to server
```
**Solution:** Ensure PostgreSQL is running and credentials in `.env` are correct.

### Module Not Found Error
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:** Run `pip install -r requirements.txt`

### Port Already in Use
```
Port 8501 is already in use
```
**Solution:** 
- Close other Streamlit applications
- OR use different port: `streamlit run app.py --server.port=8502`

## Environment Configuration

If needed, edit `.env` file:
```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/cancercare
```

## Default Credentials (Sample Data)

If you seeded sample data:
- **Admin:** username=admin, password=admin123
- **Patient:** username=john_doe, password=patient123
- **Doctor:** username=dr_smith, password=doctor123

## Features to Explore

✅ **Home Page:** Modern dark theme interface  
✅ **Prediction:** AI-powered lung cancer risk assessment  
✅ **Patients:** Patient management system  
✅ **Doctors:** Doctor portal with appointments  
✅ **Network Stats:** Real-time monitoring  

## Need Help?

- Check README.md for detailed documentation
- Review walkthrough.md for feature details
- Examine code comments for implementation details

## Quick Tips

- **Dark Theme:** Optimized for reduced eye strain
- **Navigation:** Use sidebar or quick action buttons
- **Search:** Use search feature in Patients page
- **Statistics:** View network and appointment stats in Doctors portal
- **Charts:** Interactive Plotly visualizations

---

**Enjoy using CancerCare! 🫁**
