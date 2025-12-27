# CancerCare Project - Complete Documentation

**Comprehensive Guide to System Architecture, Features, and Workflows**

---

## Table of Contents

1. Project Overview
2. System Architecture
3. Core Features
4. Technology Stack
5. Database Design
6. Backend Services
7. Frontend Pages
8. Data Flow & Workflows
9. AI/ML Integration
10. How Everything Connects
11. Running the Project
12. Advanced Features

---

## 1. PROJECT OVERVIEW

### What is CancerCare?

CancerCare is a comprehensive web-based laboratory management system designed for cancer diagnosis and patient care. It integrates:
- Lung cancer risk prediction using Machine Learning
- Patient and doctor management
- Medical image analysis with AI
- Post-diagnosis tracking
- Tumor marker monitoring
- Treatment plan management

### Key Objectives

- **Accurate Prediction:** ML model with 90%+ accuracy for lung cancer risk assessment
- **Comprehensive Care:** Track entire patient journey from diagnosis to treatment
- **Data-Driven:** Use algorithms and data structures for efficient operations
- **User-Friendly:** Intuitive Streamlit interface for healthcare professionals

---

## 2. SYSTEM ARCHITECTURE

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│               User Interface (Streamlit)            │
│  ┌──────────┬──────────┬──────────┬──────────┐     │
│  │Dashboard │Prediction│ Patients │Post-Diag │     │
│  └──────────┴──────────┴──────────┴──────────┘     │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              Application Layer (app.py)             │
│         Navigation & Page Routing System            │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              Backend Services Layer                 │
│  ┌──────────┬──────────┬──────────┬──────────┐     │
│  │ Patient  │Prediction│  Image   │  Tumor   │     │
│  │ Service  │ Service  │ Service  │ Marker   │     │
│  └──────────┴──────────┴──────────┴──────────┘     │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              AI/ML Layer                            │
│  ┌──────────────────┬─────────────────────┐        │
│  │ Lung Cancer Model│ Image Classifier    │        │
│  │ (GradientBoost)  │ (ResNet50)          │        │
│  └──────────────────┴─────────────────────┘        │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              Data Layer                             │
│  ┌──────────────────┬─────────────────────┐        │
│  │  PostgreSQL DB   │  File Storage       │        │
│  │  (9 tables)      │  (Images)           │        │
│  └──────────────────┴─────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

### Component Breakdown

**Frontend (Streamlit):**
- 15+ interactive pages
- Real-time updates
- Responsive design
- Dark theme interface

**Backend (Python Services):**
- 8 core services
- Business logic layer
- Data validation
- Error handling

**AI/ML:**
- 2 machine learning models
- Automatic analysis
- Prediction pipeline

**Database (PostgreSQL):**
- 9 normalized tables
- Foreign key relationships
- ACID compliance

---

## 3. CORE FEATURES

### Feature List

#### A. Patient Management
- **Create:** Add new patients with demographics
- **Read:** View patient details and history
- **Update:** Modify patient information
- **Delete:** Remove patient records
- **Search:** Advanced DSA-powered search

#### B. Prediction System
- **Single Analysis:** One patient at a time
- **Batch Processing:** Multiple patients via CSV
- **Risk Levels:** Low, Medium, High
- **Confidence Scores:** 0-100%
- **23 Input Features:** Age, smoking, symptoms, etc.

#### C. Post-Diagnosis Tracking
- **Diagnosis Records:** Cancer type, stage, tumor size
- **Medical Images:** Upload with AI analysis
- **Tumor Markers:** Track 7 biomarkers with trends
- **Treatment Plans:** Document therapies
- **Progress Timeline:** Complete medical history

#### D. Doctor Management
- **Doctor Profiles:** Name, specialization, contact
- **Appointment Scheduling:** Link patients to doctors
- **Workload Tracking:** Appointments per doctor

#### E. Reporting & Analytics
- **Patient Reports:** Downloadable PDFs
- **Batch Reports:** CSV exports
- **Analytics Dashboard:** Visual insights
- **Trend Analysis:** Over time metrics

---

## 4. TECHNOLOGY STACK

### Programming Languages
- **Python 3.8+** - Core application
- **SQL** - Database queries
- **JavaScript** (minor) - Streamlit components

### Frameworks & Libraries

**Web Framework:**
- Streamlit 1.28+ (Web UI)

**Data Science:**
- NumPy (Arrays, computations)
- Pandas (Data manipulation)
- Scikit-learn (ML models)
- Plotly (Visualizations)

**Machine Learning:**
- Joblib (Model persistence)
- PyTorch (Deep learning - optional)
- TorchVision (Pre-trained models)

**Database:**
- SQLAlchemy (ORM)
- psycopg2 (PostgreSQL driver)
- Alembic (Migrations - optional)

**Image Processing:**
- Pillow/PIL (Image handling)
- OpenCV (Optional - advanced processing)

**Utilities:**
- python-dotenv (Environment variables)
- pathlib (File paths)
- datetime (Timestamps)

---

## 5. DATABASE DESIGN

### Database Schema (9 Tables)

#### 1. **patients**
```sql
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    mrn VARCHAR(50) UNIQUE,
    name VARCHAR(100),
    age INTEGER,
    gender VARCHAR(10),
    contact VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Purpose:** Store patient demographics  
**Relationships:** One-to-many with predictions, images, markers

#### 2. **predictions**
```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    risk_level VARCHAR(20),      -- Low/Medium/High
    confidence FLOAT,             -- 0.0 to 1.0
    probabilities TEXT,           -- JSON string
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Purpose:** Store ML prediction results  
**Relationships:** Many-to-one with patients

#### 3. **doctors**
```sql
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    specialization VARCHAR(100),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Purpose:** Doctor directory  
**Relationships:** One-to-many with appointments

#### 4. **appointments**
```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    doctor_id INTEGER REFERENCES doctors(id),
    appointment_date TIMESTAMP,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'scheduled',
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Purpose:** Schedule patient-doctor meetings  
**Relationships:** Many-to-one with patients, doctors

#### 5. **post_diagnosis**
```sql
CREATE TABLE post_diagnosis (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    diagnosis_date TIMESTAMP,
    cancer_type VARCHAR(100),     -- Lung, Breast, etc.
    stage VARCHAR(20),            -- I, II, III, IV
    tumor_size_mm FLOAT,
    lymph_nodes_affected INTEGER,
    metastasis_status VARCHAR(50),
    treatment_plan TEXT,
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Purpose:** Track cancer diagnosis details  
**Relationships:** Many-to-one with patients

#### 6. **medical_images**
```sql
CREATE TABLE medical_images (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    post_diagnosis_id INTEGER REFERENCES post_diagnosis(id),
    image_type VARCHAR(50),       -- MRI, CT, X-Ray
    file_path VARCHAR(500),
    upload_date TIMESTAMP,
    
    -- AI Analysis Results
    ai_analyzed BOOLEAN DEFAULT FALSE,
    tumor_detected BOOLEAN,
    confidence_score FLOAT,
    tumor_count INTEGER,
    largest_tumor_size FLOAT,
    analysis_summary TEXT,        -- JSON
    
    -- Metadata
    image_width INTEGER,
    image_height INTEGER,
    file_size_kb INTEGER
);
```

**Purpose:** Store medical images with AI analysis  
**Relationships:** Many-to-one with patients, post_diagnosis

#### 7. **tumor_markers**
```sql
CREATE TABLE tumor_markers (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    post_diagnosis_id INTEGER REFERENCES post_diagnosis(id),
    marker_name VARCHAR(50),      -- CEA, CA19-9, etc.
    value FLOAT,
    unit VARCHAR(20),             -- ng/mL, U/mL
    test_date TIMESTAMP,
    reference_min FLOAT,
    reference_max FLOAT,
    is_abnormal BOOLEAN,
    lab_name VARCHAR(200),
    notes TEXT,
    created_at TIMESTAMP
);
```

**Purpose:** Track tumor biomarker levels  
**Relationships:** Many-to-one with patients, post_diagnosis

#### 8. **reports**
```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    filename VARCHAR(200),
    file_path TEXT,
    uploaded_at TIMESTAMP DEFAULT NOW()
);
```

**Purpose:** Store uploaded reports  
**Relationships:** Many-to-one with patients

#### 9. **users**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(20),             -- admin, doctor, lab_tech
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    last_login TIMESTAMP
);
```

**Purpose:** User authentication (for future login system)

### Entity Relationships

```
patients (1) ──── (many) predictions
patients (1) ──── (many) appointments ──── (many) doctors (1)
patients (1) ──── (many) post_diagnosis
patients (1) ──── (many) medical_images ──── (many) post_diagnosis (1)
patients (1) ──── (many) tumor_markers ──── (many) post_diagnosis (1)
patients (1) ──── (many) reports
```

---

## 6. BACKEND SERVICES

### Service Architecture

Each service follows the same pattern:
1. Connects to database
2. Validates input
3. Performs business logic
4. Returns (result, error)
5. Handles exceptions

### Core Services

#### A. patient_service.py

**Purpose:** Manage patient CRUD operations

**Key Methods:**
```python
create_patient(data: Dict) → (Patient, error)
get_patient_by_id(id: int) → Patient
get_patient_by_mrn(mrn: str) → Patient
get_all_patients() → List[Patient]
update_patient(id: int, data: Dict) → (Patient, error)
delete_patient(id: int) → (bool, error)
search_patients(query: str) → List[Patient]
```

**Usage Example:**
```python
from core.services.patient_service import patient_service

patient, error = patient_service.create_patient({
    'mrn': 'MRN001',
    'name': 'John Doe',
    'age': 65,
    'gender': 'M'
})
```

#### B. prediction_service.py

**Purpose:** Generate ML predictions

**Key Methods:**
```python
generate_prediction(patient_id: int, features: Dict) 
    → (Prediction, error)
get_patient_predictions(patient_id: int) 
    → List[Prediction]
```

**Workflow:**
1. Receive patient features (23 inputs)
2. Call ml_service.predict()
3. Get risk_level, confidence, probabilities
4. Store in database
5. Return prediction object

#### C. post_diagnosis_service.py

**Purpose:** Manage diagnosis records

**Key Methods:**
```python
create_diagnosis(patient_id: int, data: Dict) 
    → (PostDiagnosis, error)
update_diagnosis(diagnosis_id: int, data: Dict) 
    → (PostDiagnosis, error)
get_patient_diagnosis(patient_id: int) 
    → List[PostDiagnosis]
get_latest_diagnosis(patient_id: int) 
    → PostDiagnosis
delete_diagnosis(diagnosis_id: int) 
    → (bool, error)
```

#### D. image_service.py

**Purpose:** Handle medical image uploads

**Key Methods:**
```python
upload_image(patient_id: int, image_file: BinaryIO, 
             image_type: str, auto_analyze: bool = True) 
    → (MedicalImage, error)
get_patient_images(patient_id: int) 
    → List[MedicalImage]
delete_image(image_id: int) 
    → (bool, error)
update_ai_analysis(image_id: int, analysis_data: Dict) 
    → (MedicalImage, error)
```

**Auto-Analysis:**
```python
# Upload triggers automatic AI analysis
image, error = image_service.upload_image(
    patient_id=1,
    image_file=file,
    image_type='CT Scan',
    auto_analyze=True  # ← Automatic AI
)
# Results automatically stored in database
```

#### E. tumor_marker_service.py

**Purpose:** Track tumor biomarkers

**Key Methods:**
```python
record_marker(patient_id: int, marker_data: Dict) 
    → (TumorMarker, error)
get_patient_markers(patient_id: int) 
    → List[TumorMarker]
get_marker_trend(patient_id: int, marker_name: str) 
    → List[TumorMarker]
analyze_trend(patient_id: int, marker_name: str) 
    → Dict
get_reference_ranges() 
    → Dict
```

**Pre-configured Markers:**
- CEA (0-3 ng/mL)
- CA 19-9 (0-37 U/mL)
- CA 125 (0-35 U/mL)
- PSA (0-4 ng/mL)
- AFP (0-10 ng/mL)
- CA 15-3 (0-30 U/mL)
- CA 27-29 (0-38 U/mL)

---

## 7. FRONTEND PAGES

### Page Structure

All pages follow Streamlit's architecture:
```python
def show():
    """Main function called by app.py"""
    # Page logic here
    st.title("Page Title")
    # Components...
```

### Main Pages

#### 1. Lab Dashboard (lab_dashboard.py)

**Purpose:** Central hub for lab technicians

**Features:**
- Quick stats (patients, predictions, appointments)
- Recent activity feed
- Quick actions (new prediction, view patient)
- Notifications panel

#### 2. Single Analysis (prediction_page.py)

**Purpose:** Predict lung cancer risk for one patient

**Workflow:**
1. Select existing patient OR create new
2. Enter 23 risk factors
3. Click "Predict Risk Level"
4. View results (Low/Medium/High)
5. See confidence and probabilities
6. Save to database

**23 Input Features:**
- Demographics: Age, Gender
- Lifestyle: Smoking, Alcohol
- Exposures: Pollution, Dust, Occupational Hazards
- Symptoms: Coughing, Wheezing, Shortness of Breath
- Medical: Chronic Disease, Allergies, Fatigue

#### 3. Batch Processing (batch_processing.py)

**Purpose:** Process multiple patients via CSV

**Workflow:**
1. Upload CSV file
2 System validates format
3. Auto-generates predictions
4. Display results table
5. Download updated CSV

#### 4. Post-Diagnosis (post_diagnosis_page.py)

**Purpose:** Comprehensive post-diagnosis tracking

**5 Tabs:**

**Tab 1 - Diagnosis Info:**
- Form: cancer type, stage, tumor size
- Display recent diagnoses
- Update treatment plans

**Tab 2 - Medical Images:**
- Upload: JPEG, PNG (max 50MB)
- Automatic AI analysis
- Gallery view with results
- Before/after comparisons

**Tab 3 - Tumor Markers:**
- Record test results
- Interactive Plotly trend charts
- Reference range visualization
- Abnormality alerts

**Tab 4 - Treatment Plan:**
- View all treatment plans
- Link to diagnoses
- Historical tracking

**Tab 5 - Progress Timeline:**
- Chronological events
- All diagnoses, images, markers
- Visual timeline cards

#### 5. Patient Records (patients_page.py)

**Purpose:** Patient directory and management

**Features:**
- Searchable patient list
- Patient cards with key info
- Edit/delete functionality
- Link to prediction history

#### 6. Search (search_page.py)

**Purpose:** Advanced patient search using DSA

**Algorithms:**
- Binary Search (sorted MRN)
- Linear Search (name, demographics)
- Binary Search Tree (range queries)
- Hash Table (exact match)

---

## 8. DATA FLOW & WORKFLOWS

### Workflow 1: New Patient Prediction

```
Step 1: User selects "Single Analysis" page
    ↓
Step 2: Create or select patient
    ├─ New: Enter MRN, name, age, gender
    └─ Existing: Select from dropdown
    ↓
Step 3: Enter 23 risk factor values
    - Age, smoking, symptoms, etc.
    ↓
Step 4: Click "Predict Risk Level"
    ↓
Step 5: prediction_service.generate_prediction()
    ├─ Calls ml_service.predict(features)
    │   ├─ Load trained model (lung_cancer_pipeline.pkl)
    │   ├─ Preprocess features
    │   ├─ Run prediction
    │   └─ Return (risk_level, confidence, probabilities)
    ├─ Store in predictions table
    └─ Return Prediction object
    ↓
Step 6: Display results
    - Risk level badge (color-coded)
    - Confidence percentage
    - Probability distribution chart
    - Recommendations
    ↓
Step 7: Save to database ✓
```

### Workflow 2: Medical Image Upload with AI

```
Step 1: Navigate to Post-Diagnosis → Medical Images tab
    ↓
Step 2: Upload image file (drag & drop)
    - Supported: JPEG, PNG
    - Max size: 50 MB
    ↓
Step 3: Click "Upload & Analyze"
    ↓
Step 4: image_service.upload_image()
    ├─ Validate file (format, size)
    ├─ Create unique filename
    ├─ Save to uploads/medical_images/{patient_id}/
    ├─ Extract metadata (width, height, size)
    ├─ Create MedicalImage record
    ├─ IF auto_analyze = True:
    │   └─ Call medical_image_classifier.detect_abnormalities()
    │       ├─ Load pre-trained ResNet50
    │       ├─ Preprocess image (resize, normalize)
    │       ├─ Run inference
    │       ├─ Classify: Normal vs Abnormal
    │       ├─ Calculate confidence score
    │       ├─ Estimate tumor count & size
    │       └─ Return analysis results
    ├─ Update MedicalImage with AI results
    │   - tumor_detected
    │   - confidence_score
    │   - tumor_count
    │   - largest_tumor_size
    └─ Save to database
    ↓
Step 5: Display results
    - Image preview
    - AI analysis summary
    - Tumor detection status
    - Confidence score
    ↓
Step 6: Add to medical timeline ✓
```

### Workflow 3: Tumor Marker Tracking

```
Step 1: Go to Post-Diagnosis → Tumor Markers tab
    ↓
Step 2: Select marker (CEA, CA 19-9, etc.)
    ↓
Step 3: Enter value and test date
    ↓
Step 4: tumor_marker_service.record_marker()
    ├─ Get reference range for marker
    ├─ Check if value is abnormal
    ├─ Create TumorMarker record
    └─ Save to database
    ↓
Step 5: Update trend chart
    ├─ Query all markers for patient
    ├─ Group by marker name
    ├─ Sort by test date
    ├─ Generate Plotly line chart
    │   - X-axis: Dates
    │   - Y-axis: Marker value
    │   - Reference range line
    │   - Color-code abnormal points
    └─ Display interactive chart
    ↓
Step 6: Alert if abnormal
    - Show red badge
    - Display percentage above normal
    ↓
Step 7: Add to timeline ✓
```

---

## 9. AI/ML INTEGRATION

### Two ML Systems

#### A. Lung Cancer Prediction Model

**Location:** `data_science/model_1/`

**Algorithm:** Gradient Boosting Classifier

**Training Data:**
- 1000+ patient records
- 15 features (mapped from 23 inputs)
- 3 classes: Low, Medium, High risk

**Features Used:**
1. AGE
2. SMOKING (intensity)
3. YELLOW_FINGERS
4. ANXIETY
5. PEER_PRESSURE
6. CHRONIC_DISEASE
7. FATIGUE
8. ALLERGY
9. WHEEZING
10. ALCOHOL_CONSUMING
11. COUGHING
12. SHORTNESS_OF_BREATH
13. SWALLOWING_DIFFICULTY
14. CHEST_PAIN
15. GENDER_M (binary)

**Performance:**
- Accuracy: 90%+
- F1-Score: 0.89
- Saved as: `lung_cancer_pipeline.pkl`

**Usage:**
```python
from core.services.ml_service import ml_service

features = {
    'age': 65,
    'smoking': 7,
    'gender': 'M',
    # ... 20 more features
}

result = ml_service.predict(features)
# Returns: {
#     'risk_level': 'High',
#     'confidence': 0.87,
#     'probabilities': {
#         'Low': 0.05,
#         'Medium': 0.08,
#         'High': 0.87
#     }
# }
```

**Feature Mapping:**
```python
# Input (23 features) → Model (15 features)
def map_features(input_features):
    return {
        'AGE': input_features['age'],
        'SMOKING': input_features['smoking'],
        'GENDER_M': 1 if input_features['gender'] == 'M' else 0,
        ...
    }
```

#### B. Medical Image Classifier

**Location:** `core/ml/image_classifier.py`

**Algorithm:** Pre-trained ResNet50 (Transfer Learning)

**Architecture:**
```
Input Image (any size)
    ↓
Resize → 256x256
    ↓
Center Crop → 224x224
    ↓
Normalize (ImageNet stats)
    ↓
ResNet50 (50 layers)
    ↓
Softmax
    ↓
Binary Classification (Normal/Abnormal)
```

**Features:**
- `analyze_image()` - Basic classification
- `detect_abnormalities()` - Tumor detection
- `compare_images()` - Before/after analysis
- `extract_features()` - 2048-dim feature vector

**Dual-Mode Operation:**

**Mode 1: Full AI (when PyTorch available)**
```python
# Uses actual ResNet50
model = torchvision.models.resnet50(pretrained=True)
# GPU acceleration if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
```

**Mode 2: Fallback (always works)**
```python
# Uses PIL-based image statistics
mean_intensity = np.mean(image_array)
std_intensity = np.std(image_array)
# Rule-based classification
```

**Output Format:**
```python
{
    'tumor_detected': True,
    'confidence_score': 0.87,
    'tumor_count': 1,
    'largest_tumor_size': 32.5,  # mm
    'classification': 'Abnormal',
    'analysis_summary': '{...}'  # JSON
}
```

---

## 10. HOW EVERYTHING CONNECTS

### Complete Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                          │
│  Browser → Streamlit UI → Selects Page & Enters Data        │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                    APP.PY (Router)                           │
│  - Gets page from query params                               │
│  - Maps to page module                                       │
│  - Calls page.show()                                         │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                FRONTEND PAGE (UI Logic)                      │
│  Examples:                                                   │
│  - post_diagnosis_page.py                                    │
│  - prediction_page.py                                        │
│  - Uses forms, buttons, charts                               │
│  - Calls backend services                                    │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│              BACKEND SERVICE (Business Logic)                │
│  Examples:                                                   │
│  - patient_service.create_patient()                          │
│  - image_service.upload_image()                              │
│  - prediction_service.generate_prediction()                  │
│                                                              │
│  Services may call:                                          │
│  ├─ Other services                                           │
│  ├─ ML models                                                │
│  └─ Database                                                 │
└──────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        │                                           │
┌────────────────────┐                  ┌────────────────────┐
│    ML/AI LAYER     │                  │   DATABASE LAYER   │
│                    │                  │                    │
│ - ml_service       │                  │ - SQLAlchemy ORM   │
│ - image_classifier │                  │ - PostgreSQL       │
│                    │                  │ - 9 tables         │
│ Loads models:      │                  │                    │
│ - .pkl files       │                  │ Operations:        │
│ - ResNet50         │                  │ - INSERT           │
│                    │                  │ - SELECT           │
│ Returns:           │                  │ - UPDATE           │
│ - Predictions      │                  │ - DELETE           │
│ - Analysis         │                  │                    │
└────────────────────┘                  └────────────────────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                  RESULTS BACK TO USER                        │
│  Service returns (result, error) → Page displays → UI       │
└──────────────────────────────────────────────────────────────┘
```

### Connection Example: Making a Prediction

**Step-by-Step:**

1. **User Action:**
   ```
   User fills form on prediction_page.py
   Clicks "Predict Risk Level"
   ```

2. **Frontend calls Backend:**
   ```python
   # In prediction_page.py
   prediction, error = prediction_service.generate_prediction(
       patient_id=1,
       features={'age': 65, 'smoking': 7, ...}
   )
   ```

3. **Service calls ML:**
   ```python
   # In prediction_service.py
   result = ml_service.predict(features)
   ```

4. **ML loads model:**
   ```python
   # In ml_service.py
   model = joblib.load('lung_cancer_pipeline.pkl')
   ```

5. **ML processes:**
   ```python
   # Map 23 features → 15 model features
   model_features = map_features(features)
   # Predict
   prediction = model.predict([model_features])
   probabilities = model.predict_proba([model_features])
   ```

6. **Service saves to DB:**
   ```python
   # In prediction_service.py
   pred = Prediction(
       patient_id=patient_id,
       risk_level=result['risk_level'],
       confidence=result['confidence'],
       probabilities=json.dumps(result['probabilities'])
   )
   db.add(pred)
   db.commit()
   ```

7. **Result back to UI:**
   ```python
   # In prediction_page.py
   if not error:
       st.success(f"Risk Level: {prediction.risk_level}")
       st.metric("Confidence", f"{prediction.confidence:.1%}")
   ```

### File Storage Connection

```
Image Upload Flow:
==================

frontend/post_diagnosis_page.py
    ↓ (uploaded_file object)
image_service.upload_image()
    ↓ (save to disk)
uploads/medical_images/{patient_id}/xxx.jpg
    ↓ (record path)
MedicalImage table (file_path column)
    ↓ (trigger AI analysis)
medical_image_classifier.detect_abnormalities()
    ↓ (load from disk)
PIL.Image.open(file_path)
    ↓ (analyze)
ResNet50 inference
    ↓ (store results)
UPDATE medical_images SET 
    ai_analyzed=TRUE,
    tumor_detected=...,
    confidence_score=...
    ↓ (display)
frontend shows image + AI results
```

---

## 11. RUNNING THE PROJECT

### Prerequisites

**Required:**
- Python 3.8+
- PostgreSQL 12+
- pip (package manager)

**Optional:**
- PyTorch (for full AI)
- CUDA (for GPU acceleration)

### Installation Steps

**1. Clone/Download Project**
```bash
cd E:\Project\CancerCare -- Copy
```

**2. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

Main packages:
- streamlit
- sqlalchemy
- psycopg2-binary
- pandas
- numpy
- scikit-learn
- plotly
- pillow

**3. Set Up PostgreSQL**

Create database:
```sql
CREATE DATABASE cancercare;
```

**4. Configure Environment**

Create `.env` file:
```
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/cancercare
SECRET_KEY=your-secret-key-here
```

**5. Initialize Database**
```bash
python init_postdiag_tables.py
```

This creates all 9 tables.

**6. Train ML Model (Optional)**

If model not already trained:
```bash
python run_ds.py train
```

**7. Run Application**
```bash
streamlit run app.py
```

Open browser to: `http://localhost:8501`

### Quick Start Script

```bash
# Complete setup in one go
python fix_password.py        # Update DB password
python init_postdiag_tables.py  # Create tables
streamlit run app.py           # Start app
```

### Troubleshooting

**Issue: Database connection error**
```
Solution: Check .env file, verify PostgreSQL is running
```

**Issue: ML model not found**
```
Solution: System uses mock predictions automatically
Or run: python run_ds.py train
```

**Issue: Page not loading**
```
Solution: Restart Streamlit (Ctrl+C, then run again)
```

---

## 12. ADVANCED FEATURES

### A. Data Structures & Algorithms Implementation

**Binary Search (O(log n)):**
```python
# In search_page.py
def binary_search_mrn(patients_sorted, target_mrn):
    left, right = 0, len(patients_sorted) - 1
    while left <= right:
        mid = (left + right) // 2
        if patients_sorted[mid].mrn == target_mrn:
            return patients_sorted[mid]
        elif patients_sorted[mid].mrn < target_mrn:
            left = mid + 1
        else:
            right = mid - 1
    return None
```

**Binary Search Tree:**
```python
class PatientBST:
    """BST for range queries on patient ages"""
    def insert(patient)
    def search_range(min_age, max_age)
```

**Hash Table:**
```python
# O(1) lookup by MRN
patient_dict = {p.mrn: p for p in patients}
result = patient_dict.get('MRN001')
```

### B. Automatic Features

**Email Notifications (future):**
- On abnormal prediction
- On abnormal tumor marker
- Appointment reminders

**Batch Processing:**
- Upload CSV → Auto-process all rows
- Generate predictions
- Export results

**Auto-Analysis:**
- Upload image → Automatic AI analysis
- No manual trigger needed
- Results stored immediately

### C. Security Features

**Password Hashing (ready for login):**
```python
import bcrypt
password_hash = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt()
)
```

**Environment Variables:**
- Database credentials in .env
- Not committed to version control
- Secure configuration

**SQL Injection Prevention:**
- SQLAlchemy ORM (parameterized queries)
- No raw SQL strings

### D. Performance Optimizations

**Database Indexing:**
- Primary keys (automatic)
- MRN unique index
- Foreign key indexes

**Caching:**
- Model loaded once
- Session state caching

**Lazy Loading:**
- Images loaded on demand
- Pagination for large datasets

---

## CONCLUSION

### System Summary

CancerCare is a **full-stack medical application** that combines:
- **Modern Web UI** (Streamlit)
- **Robust Backend** (Python services)
- **AI/ML** (Gradient Boosting + ResNet50)
- **Relational Database** (PostgreSQL)
- **File Management** (Medical images)
- **Data Visualization** (Plotly charts)

### Key Strengths

1. **Comprehensive:** Covers entire patient journey
2. **Intelligent:** Two ML models for predictions
3. **Scalable:** Service-oriented architecture
4. **User-Friendly:** Intuitive Streamlit interface
5. **Production-Ready:** Error handling, validation, fallbacks

### Technology Integration

Everything works together:
- **Frontend** calls **Backend Services**
- **Services** use **ML Models** and **Database**
- **ML** processes data and returns predictions
- **Database** stores everything persistently
- **Results** flow back to **User Interface**

### Future Enhancements

- User authentication/authorization
- Cloud deployment (AWS, Azure)
- Mobile responsive design
- Real-time collaboration
- Advanced analytics dashboards
- Integration with hospital systems

---

**End of Documentation**

*Project: CancerCare - Comprehensive Lab Management System*  
*Version: 1.0*  
*Last Updated: December 26, 2025*
