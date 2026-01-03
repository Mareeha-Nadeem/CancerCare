# SQLAlchemy Mapper Error - PERMANENT FIX

## Problem

**Error Message:**
```
When initializing mapper Mapper[Patient(patients)], expression 'Report' failed to locate a name ('Report'). 
If this is a class name, consider adding this relationship() to the <class 'core.models.Patient'> class after both dependent classes have been defined.
```

## Root Cause

SQLAlchemy uses **string-based relationships** in `models.py`:
```python
class Patient(Base):
    reports = relationship("Report", back_populates="patient")
```

When SQLAlchemy tries to resolve these relationships, it needs the actual `Report` class to exist in memory. If the `Report` class hasn't been imported yet, it fails.

## Previous Attempts (Why They Failed)

### Attempt 1: Import in init_database()
```python
def init_database():
    from core.models import Base, Patient, Report, ...
    Base.metadata.create_all(engine)
```
**Problem:** `init_database()` is called AFTER models are already accessed elsewhere, so the error occurs before this function runs.

### Attempt 2: Restart Streamlit
**Problem:** Only a temporary fix. The error returns because the root cause wasn't addressed.

## PERMANENT SOLUTION

### File: `core/db_config.py`

**Import all models at MODULE LEVEL** (after engine creation, before any functions):

```python
# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)

# CRITICAL FIX: Import all models at module level to resolve SQLAlchemy relationships
# This ensures all model classes are loaded before any code tries to use them
# This MUST happen after engine creation but before any code uses the models
from core.models import (
    Base, Patient, Report, Prediction, Doctor, Appointment,
    User, PostDiagnosis, MedicalImage, TumorMarker
)
```

## Why This Works

1. **Module-level import** happens when `db_config` is first imported
2. This happens **BEFORE** any code tries to use the models
3. All model classes are registered with SQLAlchemy's mapper
4. When relationships are resolved, all classes already exist
5. No more "failed to locate a name" error!

## Import Order (Critical)

```
1. Create SQLAlchemy engine
2. Create session factory
3. Import ALL models (THIS IS KEY!)
4. Define helper functions (get_db, init_database)
5. Application code can now safely use models
```

## Benefits

- **Permanent**: Fix survives restarts
- **Automatic**: No need to call special functions
- **Safe**: Models always loaded in correct order
- **Clean**: No circular import issues

## Testing

After applying fix:
1. Stop Streamlit: `Ctrl+C`
2. Restart: `streamlit run app.py`
3. Login should work without errors
4. Check logs for: No mapper errors

## Files Modified

- `core/db_config.py` - Added module-level model imports

## Future-Proof

If you add NEW models:
1. Define them in `core/models.py`
2. Add to import in `core/db_config.py` line 33-36
3. Restart application

## Example of Correct db_config.py

```python
"""
Database Configuration - Works with SQLite or PostgreSQL
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pathlib import Path

# 1. Load environment
from dotenv import load_dotenv
load_dotenv()

# 2. Get database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cancercare.db")

# 3. Create engine
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# 4. Create session factory  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)

# 5. CRITICAL: Import ALL models at module level
from core.models import (
    Base, Patient, Report, Prediction, Doctor, Appointment,
    User, PostDiagnosis, MedicalImage, TumorMarker
)

# 6. Define helper functions
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_database():
    Base.metadata.create_all(engine)
```

## Summary

**Problem:** Mapper can't find model classes  
**Solution:** Import all models at module level in `db_config.py`  
**Result:** Error permanently resolved  
**Status:** FIXED 
