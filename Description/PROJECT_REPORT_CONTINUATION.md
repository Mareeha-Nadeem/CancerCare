# CANCERCARE PROJECT REPORT - CONTINUATION
## Detailed Feature Workflows and System Methodologies

This document continues the comprehensive project report with detailed explanations of workflows, features, and system operations.

---

## BATCH PROCESSING WORKFLOW (CONTINUED)

### CSV Data Preparation

**User prepares data file offline:**

**Column Requirements:**
File must contain these exact column headers (order doesn't matter):
- mrn (Medical Record Number - unique identifier)
- name (Patient full name)
- age (Numeric, 0-150)
- gender (M or F)
- smoking (1-10 scale of intensity)
- alcohol (1-10 scale)
- yellow_fingers (0=No, 1=Yes)
- anxiety (1-10 scale)
- peer_pressure (1-10 scale)
- chronic_disease (0=No, 1=Yes)
- fatigue (0=No, 1=Yes)
- allergy (0=No, 1=Yes)
- wheezing (0=No, 1=Yes)
- coughing (0=No, 1=Yes)
- shortness_of_breath (0=No, 1=Yes)
- swallowing_difficulty (0=No, 1=Yes)
- chest_pain (0=No, 1=Yes)
- coughing_blood (0=No, 1=Yes)
- passive_smoker (0=No, 1=Yes)
- dust_allergy (0=No, 1=Yes)
- occupational_hazards (0=No, 1=Yes)
- genetic_risk (0=No, 1=Yes)
- balanced_diet (0=No, 1=Yes)

**Sample CSV Content:**
```
mrn,name,age,gender,smoking,alcohol,yellow_fingers,anxiety,peer_pressure,chronic_disease,fatigue,allergy,wheezing,coughing,shortness_of_breath,swallowing_difficulty,chest_pain,coughing_blood,passive_smoker,dust_allergy,occupational_hazards,genetic_risk,balanced_diet
MRN001,John Doe,65,M,8,5,1,6,3,1,1,0,1,1,1,0,1,0,1,1,1,0,0
MRN002,Jane Smith,52,F,2,1,0,4,2,0,0,1,0,1,0,0,0,0,0,1,0,1,1
MRN003,Bob Johnson,71,M,9,7,1,8,5,1,1,1,1,1,1,1,1,1,1,1,1,0,0
```

### Upload and Validation

**Step-by-Step Upload Process:**

**Upload Interface:**
User sees drag-and-drop zone or file browse button, accepts only .csv files, shows file name after selection, displays file size for verification.

**File Transmission:**
File uploaded to server, progress bar shows upload status (for large files), temporary storage before processing begins, file available to backend services.

**Initial Validation:**
System performs comprehensive checks:

**Check 1: File Format**
- Must be valid CSV structure
- Comma-separated values
- Proper line endings (handles Windows/Unix/Mac)
- UTF-8 encoding

**Check 2: Header Validation**
- First row must contain column headers
- All 23 required columns must be present
- Column names must match exactly (case-insensitive)
- Order doesn't matter
- Extra columns ignored (allows for notes columns)

**Check 3: Data Type Validation**
For each row:
- **mrn:** String, length 1-50, non-empty
- **name:** String, length 2-100, contains letters
- **age:** Integer, range 0-150
- **gender:** Must be 'M', 'F', or 'Male', 'Female'
- **Numeric scales (1-10):** Integer, range 1-10
- **Binary fields (0/1):** Integer, must be 0 or 1
- **Boolean fields:** Accept Yes/No, True/False, 1/0

**Check 4: Business Logic V
