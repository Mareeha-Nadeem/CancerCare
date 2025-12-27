# Default Admin Credentials

## IMPORTANT: No Default Account

**There is NO default admin username/password.**

You must create an account first by signing up.

## How to Create Admin Account:

1. Run: `streamlit run app.py`
2. Click **"Sign Up"** on landing page
3. Fill in form:
   - **Username:** `admin` (or your choice)
   - **Email:** `admin@cancercare.com`
   - **Password:** `admin123` (or your choice - min 6 chars)
   - **Role:** Select `admin`
4. Click **"Create Account"**
5. You'll be automatically logged in

## After Creating Account:

**Login credentials you created:**
- **Username:** `admin` (what you chose)
- **Password:** `admin123` (what you chose)

These credentials are stored securely in your PostgreSQL database with bcrypt hashing.

## Recommended Default:
```
Username: admin
Password: admin123
Email: admin@cancercare.com
Role: admin
```

But you can use any credentials you prefer!
