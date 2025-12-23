# 🫁 CancerCare - Lung Cancer Risk Prediction System

A comprehensive full-stack web application for lung cancer risk assessment, integrating Machine Learning, Database Management, Computer Networks, and Data Structures & Algorithms.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Course Integration](#-course-integration)
- [Screenshots](#-screenshots)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🤖 AI-Powered Predictions
- Advanced machine learning model trained on comprehensive medical data
- Real-time risk assessment with confidence scores
- Detailed probability distributions for Low, Medium, and High risk levels
- Personalized recommendations based on risk level

### 👥 Patient Management
- Complete CRUD operations for patient records
- Medical Record Number (MRN) tracking
- Search functionality for quick patient lookup
- Prediction history tracking per patient

### 👨‍⚕️ Doctor Portal
- Doctor registration and management
- Appointment scheduling with priority queuing
- Appointment status tracking (scheduled, completed, cancelled)
- Statistics dashboard

### 🌐 Computer Networks Features
- **HTTP Request/Response Logging**: Track all API interactions
- **Network Performance Monitoring**: Real-time system metrics
- **JWT Authentication**: Secure token-based authentication
- **Session Management**: User session tracking and management
- **Network Statistics**: Bandwidth, latency, and throughput monitoring

### 📊 Data Structures & Algorithms
- **Priority Queue**: Appointment scheduling based on urgency
- **Binary Search Tree**: Efficient patient indexing and searching
- **Hash Tables**: Quick MRN lookups
- **Sorting Algorithms**: Patient list organization
- **Linked Lists**: Appointment history tracking

### 🎨 Modern UI/UX
- **Dark Theme**: Black background with high-contrast elements
- **Gradient Accents**: Cyan (#00d9ff) and Pink (#ff006e) gradients
- **Responsive Design**: Works on all screen sizes
- **Smooth Animations**: Hover effects and transitions
- **Interactive Charts**: Plotly visualizations

## 🛠️ Technology Stack

### Frontend
- **Streamlit**: Web application framework
- **Custom CSS**: Modern dark theme styling
- **Plotly**: Interactive data visualization
- **HTML/CSS**: Enhanced UI components

### Backend
- **Python 3.8+**: Core programming language
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database system
- **bcrypt**: Password hashing
- **PyJWT**: JSON Web Token authentication

### Machine Learning
- **scikit-learn**: ML model framework
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **imbalanced-learn**: SMOTE for class balancing

### Monitoring & Networking
- **psutil**: System and network monitoring
- **python-dotenv**: Environment configuration
- **logging**: Application logging

## 📁 Project Structure

```
CancerCare/
├── core/
│   ├── models.py                 # Database models (Patient, Doctor, Appointment, etc.)
│   ├── db_config.py              # Database configuration
│   ├── database_init.py          # Database initialization script
│   ├── auth_manager.py           # JWT authentication
│   ├── network_logger.py         # HTTP request/response logging
│   ├── network_monitor.py        # System metrics monitoring
│   ├── validation.py             # Input validation utilities
│   └── services/
│       ├── patient_service.py    # Patient CRUD operations
│       ├── doctor_service.py     # Doctor management
│       ├── appointment_service.py # Appointment scheduling
│       ├── prediction_service.py  # ML prediction integration
│       └── ml_service.py         # ML model wrapper
│
├── frontend/
│   ├── home_page.py              # Landing page
│   ├── prediction_page.py        # Risk prediction interface
│   ├── patients_page.py          # Patient management
│   ├── doctors_page.py           # Doctor portal
│   ├── about_page.py             # About information
│   ├── service_page.py           # Services overview
│   └── contact_page.py           # Contact form
│
├── data_science/
│   └── model_1/                  # ML model (unchanged)
│       ├── interface.py          # Prediction interface
│       ├── train_model.py        # Model training
│       └── models/               # Trained models
│
├── dsa/                          # Data Structures & Algorithms
│   ├── appointment_queue.py      # Priority queue
│   ├── bst.py                    # Binary search tree
│   ├── hashing.py                # Hash table implementation
│   ├── patient_dsa.py            # Patient data structures
│   └── sorting.py                # Sorting algorithms
│
├── database/                     # JSON data files
│   ├── patients.json
│   ├── doctors.json
│   └── appointments.json
│
├── static/                       # Static assets
│   ├── logo.png
│   └── lung.png
│
├── app.py                        # Main Streamlit application
├── config.py                     # Application configuration
├── setup.py                      # Setup and installation script
├── run.py                        # Quick run script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/cancercare.git
cd cancercare
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Configure Database

1. Install and start PostgreSQL
2. Create a database named `cancercare`:

```sql
CREATE DATABASE cancercare;
```

3. Update database credentials in `.env` file (or use defaults):

```env
DATABASE_URL=postgresql+psycopg2://postgres:1234@localhost:5432/cancercare
```

### Step 4: Run Setup Script

```bash
python setup.py
```

This will:
- Check Python version
- Install all dependencies
- Create `.env` file
- Initialize database tables
- Optionally seed sample data

## 💻 Usage

### Quick Start

```bash
python run.py
```

The application will open at `http://localhost:8501`

### Manual Start

```bash
streamlit run app.py --server.port=8501
```

### First-Time Setup

1. **Navigate to Home Page**: Explore features and information
2. **Add a Doctor**: Go to Doctors Portal → Add Doctor
3. **Add a Patient**: Go to Patient Management → Add Patient
4. **Make a Prediction**: 
   - Go to Prediction page
   - Enter patient information
   - Click "Predict Risk Level"
   - View results and recommendations

### Database Initialization (Standalone)

```bash
python core/database_init.py
```

## 🎓 Course Integration

This project integrates concepts from four computer science courses:

### 1. Data Structures and Algorithms (DSA)

**Implemented Structures:**
- **Priority Queue**: `dsa/appointment_queue.py`
  - Used for appointment scheduling
  - Higher priority patients scheduled first
  
- **Binary Search Tree**: `dsa/bst.py`
  - Efficient patient searching by MRN
  - O(log n) search complexity
  
- **Hash Table**: `dsa/hashing.py`
  - Quick patient lookup
  - O(1) average access time
  
- **Sorting Algorithms**: `dsa/sorting.py`
  - Patient list organization
  - Multiple sorting criteria

**Usage Example:**
```python
from dsa.patient_dsa import PatientBST
bst = PatientBST()
bst.insert(patient)
found_patient = bst.search(mrn)
```

### 2. Introduction to Data Science

**ML Pipeline:**
- Feature engineering (23+ features)
- Data preprocessing and normalization
- Model training with Gradient Boosting
- Cross-validation and evaluation
- Prediction with confidence scores

**Model Features:**
- Age, gender, smoking habits
- Environmental factors (air pollution, occupational hazards)
- Medical history (genetic risk, chronic diseases)
- Symptoms (chest pain, fatigue, coughing, etc.)

**Performance Metrics:**
- Accuracy, Precision, Recall
- F1-Score
- ROC-AUC
- Confusion Matrix

### 3. Computer Networks

**Network Features Demonstrated:**

**HTTP Protocol:**
```python
from core.network_logger import network_logger

# Log HTTP request
request_id = network_logger.log_request(
    method="POST",
    endpoint="/predict",
    client_ip="192.168.1.1"
)

# Log response
network_logger.log_response(
    request_id=request_id,
    status_code=200,
    response_time_ms=45.2
)
```

**Network Monitoring:**
```python
from core.network_monitor import network_monitor

# Get system metrics
metrics = network_monitor.get_system_metrics()
# Returns: CPU usage, memory, network I/O, etc.

# View network statistics
stats = network_logger.get_statistics()
# Returns: request count, response times, data transferred
```

**JWT Authentication:**
```python
from core.auth_manager import auth_manager

# Create token
token = auth_manager.create_access_token(user_data)

# Verify token
payload = auth_manager.verify_token(token)
```

### 4. Software Engineering

**SE Principles Applied:**
- **Modular Architecture**: Separated concerns (frontend, backend, database)
- **ORM Pattern**: SQLAlchemy for database abstraction
- **Service Layer**: Business logic separation
- **MVC Pattern**: Model-View-Controller architecture
- **Configuration Management**: Environment-based configuration
- **Error Handling**: Comprehensive error handling and validation
- **Documentation**: Code comments and README
- **Version Control**: Git-based workflow

## 📸 Screenshots

### Home Page
Modern dark-themed landing page with gradient accents and feature cards.

### Prediction Page
Interactive risk assessment with real-time ML predictions and visualizations.

### Patient Management
Comprehensive patient CRUD operations with search functionality.

### Doctor Portal
Doctor management and appointment dashboard with network statistics.

## 📚 API Documentation

### Patient Service

```python
from core.services.patient_service import patient_service

# Create patient
patient, error = patient_service.create_patient({
    'mrn': 'MRN001',
    'name': 'John Doe',
    'age': 65,
    'gender': 'M',
    'contact': '555-0123'
})

# Get patient
patient = patient_service.get_patient_by_mrn('MRN001')

# Search patients
results = patient_service.search_patients('John')

# Update patient
patient, error = patient_service.update_patient(patient_id, data)

# Delete patient
success, error = patient_service.delete_patient(patient_id)
```

### Prediction Service

```python
from core.services.prediction_service import prediction_service

# Generate prediction
features = {
    'age': 65,
    'smoking': 7,
    'genetic_risk': 6,
    # ... other features
}

prediction, error = prediction_service.generate_prediction(
    patient_id=1,
    features=features
)

# Get patient predictions
predictions = prediction_service.get_patient_predictions(patient_id)

# Get risk distribution
distribution = prediction_service.get_risk_distribution()
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
# Database
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/cancercare

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
JWT_EXPIRATION_MINUTES=1440

# Application
DEBUG=True
PORT=8501

# File Upload
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE_MB=10
```

### Database Configuration

Edit `core/db_config.py` for custom database settings.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This application is designed for **educational and research purposes only**. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical decisions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work*

## 🙏 Acknowledgments

- Scikit-learn for ML framework
- Streamlit for the web framework
- PostgreSQL community
- All course instructors and contributors

## 📞 Support

For support, email support@cancercare.edu or open an issue on GitHub.

---

**Built with ❤️ for academic excellence**