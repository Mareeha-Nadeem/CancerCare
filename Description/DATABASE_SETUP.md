# 🚀 Database Setup Guide

## Automatic Setup (RECOMMENDED)

Run this single command to set up everything:

```bash
python create_database.py
```

This wizard will:
- ✅ Ask for your PostgreSQL credentials
- ✅ Create the database automatically
- ✅ Initialize all tables via SQLAlchemy
- ✅ Update your .env file
- ✅ Optionally add sample data
- ✅ Test the connection

**Just follow the prompts!**

---

## What You'll Need

- PostgreSQL username (default: `postgres`)
- PostgreSQL password (the one you set during PostgreSQL installation)
- Host (default: `localhost`)
- Port (default: `5432`)
- Database name (default: `cancercare`)

---

## Step-by-Step Example

```bash
$ python create_database.py

PostgreSQL Username [postgres]: postgres
PostgreSQL Password: mypassword123
PostgreSQL Host [localhost]: 
PostgreSQL Port [5432]: 
Database Name [cancercare]: 

✅ Database 'cancercare' created successfully!
✅ All tables created successfully!
✅ Database setup complete!
```

---

## Tables Created

The script creates these tables automatically:

1. **patients** - Patient records
2. **doctors** - Doctor information
3. **appointments** - Appointment scheduling
4. **predictions** - ML prediction results
5. **users** - User authentication
6. **reports** - Medical reports

---

## After Setup

1. **Restart your Streamlit app:**
   ```bash
   # Press Ctrl+C to stop current app
   streamlit run app.py
   ```

2. **Verify it works:**
   - Go to http://localhost:8501
   - Navigate to Patients page
   - Should load without errors!

---

## Troubleshooting

### "Password authentication failed"
- Make sure you enter the correct PostgreSQL password
- This is the password you set during PostgreSQL installation

### "Could not connect to server"
- Make sure PostgreSQL is running
- Check Windows Services for "postgresql" service
- Start it if it's stopped

### "Database already exists"
- The script will ask if you want to use it
- Choose 'y' to use existing database

---

## Manual Alternative

If the automatic script doesn't work, you can manually:

1. **Open pgAdmin or psql**
2. **Run:**
   ```sql
   CREATE DATABASE cancercare;
   ```

3. **Then initialize tables:**
   ```bash
   python core/database_init.py
   ```

---

**That's it! The database will be connected to your project automatically.**
