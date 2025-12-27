# PostgreSQL Password Fix Guide

## Quick Fix Options

### Option 1: Update .env file with your PostgreSQL password

1. Open `.env` file in the project root
2. Change the DATABASE_URL line to match your PostgreSQL password:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_ACTUAL_PASSWORD@localhost:5432/cancercare
```

Replace `YOUR_ACTUAL_PASSWORD` with your PostgreSQL password.

### Option 2: Change PostgreSQL password to match config

If you want to keep the default password "1234":

```powershell
# Open PowerShell as Administrator
# Connect to PostgreSQL
psql -U postgres

# In psql, run:
ALTER USER postgres WITH PASSWORD '1234';

# Exit psql
\q
```

### Option 3: Use Windows Authentication (No Password)

If you set up PostgreSQL with Windows authentication:

```env
DATABASE_URL=postgresql+psycopg2://postgres@localhost:5432/cancercare
```

## After Fixing Password

1. **Save the .env file**
2. **Restart the Streamlit app:**
   - Press Ctrl+C in the terminal
   - Run: `streamlit run app.py`

## Quick Test

Test your connection:
```bash
python -c "from core.db_config import engine; engine.connect(); print('✅ Connected!')"
```

---

**Most Common:** Your PostgreSQL password is probably different from "1234". Just update `.env` with your actual password!
