"""
Dashboard Home Page
Main dashboard after login with stats, navbar, and quick actions
"""
import streamlit as st
from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service
from datetime import datetime, timedelta


def show():
    """Display dashboard home page"""
    
    # Check authentication
    if not st.session_state.get('authenticated', False):
        st.session_state.page = "landing"
        st.rerun()
        return
    
    # Custom CSS with teal theme
    st.markdown("""
        <style>
        /* Main app styling */
        .stApp {
            background-color: #f5f7fa;
        }
        
        /* Dashboard header */
        .dashboard-header {
            background: linear-gradient(135deg, #1e7e8c 0%, #2c9db0 100%);
            padding: 30px;
            border-radius: 15px;
            color: white;
            margin-bottom: 30px;
        }
        
        .dashboard-header h1 {
            margin: 0;
            font-size: 2.5rem;
        }
        
        .dashboard-header p {
            margin: 5px 0 0 0;
            opacity: 0.9;
        }
        
        /* Feature navbar */
        .feature-navbar {
            background: #2d3748;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            color: white;
        }
        
        .feature-navbar h3 {
            color: white;
            margin-bottom: 20px;
        }
        
        .feature-section {
            background: #374151;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
        }
        
        .feature-section h4 {
            color: #10b981;
            margin-bottom: 15px;
            font-size: 1.1rem;
        }
        
        .feature-item {
            color: #e5e7eb;
            padding: 8px 0;
            border-bottom: 1px solid #4b5563;
        }
        
        .feature-item:last-child {
            border-bottom: none;
        }
        
        /* Stat cards */
        .stat-card {
            background: var(--bg-surface-elevated);
            border-left: 5px solid #1e7e8c;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e7e8c;
            margin: 10px 0;
        }
        
        .stat-label {
            font-size: 1.1rem;
            color: #666;
            font-weight: 500;
        }
        
        /* Action cards */
        .action-card {
            background: linear-gradient(135deg, #1e7e8c 0%, #2c9db0 100%);
            border-radius: 12px;
            padding: 25px;
            color: white;
            text-align: center;
            transition: transform 0.3s ease;
            margin: 10px 0;
        }
        
        .action-card:hover {
            transform: translateY(-5px);
        }
        
        .action-title {
            font-size: 1.2rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Logout button
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Header
    username = st.session_state.get('username', 'User')
    role = st.session_state.get('user_role', 'admin').title()
    
    st.markdown(f"""
        <div class="dashboard-header">
            <h1>CancerCare Dashboard</h1>
            <p>Welcome back, <strong>{username}</strong> ({role})</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">{datetime.now().strftime('%A, %B %d, %Y')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Navbar
    st.markdown("""
        <div class="feature-navbar">
            <h3>System Features</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-section">
                <h4>Laboratory Features</h4>
                <div class="feature-item">Single Patient Risk Analysis</div>
                <div class="feature-item">Batch Processing (CSV)</div>
                <div class="feature-item">Patient History Tracking</div>
                <div class="feature-item">Reports & Export</div>
                <div class="feature-item">Lab Tech Dashboard</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-section">
                <h4>Clinical Features</h4>
                <div class="feature-item">Medical Image Upload & AI Analysis</div>
                <div class="feature-item">Tumor Marker Tracking</div>
                <div class="feature-item">Treatment Plan Management</div>
                <div class="feature-item">Progress Timeline</div>
                <div class="feature-item">Advanced Patient Search</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Get statistics
    all_patients = patient_service.get_all_patients()
    total_patients = len(all_patients) if all_patients else 0
    
    # Get recent predictions count
    recent_predictions = 0
    high_risk_count = 0
    
    for patient in (all_patients or []):
        predictions = prediction_service.get_patient_predictions(patient.id)
        if predictions:
            for pred in predictions:
                if pred.created_at and (datetime.utcnow() - pred.created_at).days <= 30:
                    recent_predictions += 1
                    if pred.risk_level == "High":
                        high_risk_count += 1
    
    # Statistics Cards
    st.markdown("### Overview Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total_patients}</div>
                <div class="stat-label">Total Patients</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{recent_predictions}</div>
                <div class="stat-label">Predictions (30d)</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{high_risk_count}</div>
                <div class="stat-label">High Risk Cases</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">91.3%</div>
                <div class="stat-label">ML Accuracy</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="action-card">
                <div class="action-title">New Prediction</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Prediction", key="action_pred", use_container_width=True):
            st.session_state.page = "prediction"
            st.query_params.page = "prediction"
            st.rerun()
    
    with col2:
        st.markdown("""
            <div class="action-card">
                <div class="action-title">View Patients</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Patients", key="action_patients", use_container_width=True):
            st.session_state.page = "patients"
            st.query_params.page = "patients"
            st.rerun()
    
    with col3:
        st.markdown("""
            <div class="action-card">
                <div class="action-title">Post-Diagnosis</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Post-Diag", key="action_postdiag", use_container_width=True):
            st.session_state.page = "post_diagnosis"
            st.query_params.page = "post_diagnosis"
            st.rerun()
    
    with col4:
        st.markdown("""
            <div class="action-card">
                <div class="action-title">Analytics</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Dashboard", key="action_dash", use_container_width=True):
            st.session_state.page = "dashboard"
            st.query_params.page = "dashboard"
            st.rerun()
    
    # System Info
    st.markdown("---")
    st.info("""
        **CancerCare System**  
       AI-Powered Cancer Diagnosis & Patient Management  
        Version 1.0 | Gradient Boosting ML + ResNet50 Deep Learning
    """)
