"""
Enhanced Lab Technician Dashboard
Primary interface for lab technicians with teal theme and navbar
"""
import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta
import plotly.graph_objects as go

from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service


def show():
    """Display lab dashboard with teal theme and navbar"""
    
    # Custom CSS matching landing page
    st.markdown("""
        <style>
        /* Match landing page colors */
        .stApp {
            background: linear-gradient(135deg, #1e7e8c 0%, #2c9db0 100%);
        }
        
        /* Header section */
        .lab-header {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            border: 3px solid rgba(255, 190, 11, 0.5);
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .lab-header h1 {
            font-size: 2.5rem;
            margin: 0;
            color: #ffbe0b;
        }
        
        /* Navigation bar */
        .navbar {
            background: #2d3748;
            padding: 15px 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .navbar h4 {
            color: white;
            width: 100%;
            margin-bottom: 10px;
        }
        
        /* Stat cards */
        .stat-card {
            background: linear-gradient(135deg, #ff006e 0%, #ffbe0b 100%);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            color: white;
            margin: 10px 0;
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: 900;
        }
        
        .stat-label {
            font-size: 1.1rem;
            margin-top: 5px;
        }
        
        /* Action cards */
        .action-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin: 10px 0;
            border: 2px solid #1e7e8c;
        }
        
        .action-card h3 {
            color: #1e7e8c;
            margin-bottom: 10px;
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
    st.markdown(f"""
        <div class="lab-header">
            <h1>Lab Technician Control Center</h1>
            <p style="font-size: 1.2rem; margin: 10px 0;">
                Your comprehensive workspace for sample analysis and risk assessment
            </p>
            <p style="font-size: 0.9rem; opacity: 0.9;">
                Logged in as: <strong>{username}</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation Bar
    st.markdown('<div class="navbar"><h4>Navigation</h4></div>', unsafe_allow_html=True)
    
    nav_cols = st.columns(7)
    nav_items = [
        ("Lab Dashboard", "lab_dashboard"),
        ("Single Analysis", "prediction"),
        ("Batch Processing", "batch_processing"),
        ("Patient History", "patient_history"),
        ("Patient Records", "patients"),
        ("Post-Diagnosis", "post_diagnosis"),
        ("Search", "search")
    ]
    
    for idx, (label, page) in enumerate(nav_items):
        with nav_cols[idx]:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.query_params.page = page
                st.rerun()
    
    # Get statistics
    try:
        all_predictions = prediction_service.get_all_predictions(limit=1000)
        today = datetime.now().date()
        today_predictions = [p for p in all_predictions if p.created_at.date() == today]
        
        all_patients = patient_service.get_all_patients(limit=1000)
        high_risk_today = [p for p in today_predictions if p.risk_level == "High"]
        pending_count = max(0, len(all_patients) - len(all_predictions))
        
        # Statistics Cards
        st.markdown("## Today's Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(today_predictions)}</div>
                    <div class="stat-label">Tests Today</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(high_risk_today)}</div>
                    <div class="stat-label">High Risk</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{pending_count}</div>
                    <div class="stat-label">Pending Samples</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(all_patients)}</div>
                    <div class="stat-label">Total Patients</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("## Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="action-card">
                    <h3>New Sample Analysis</h3>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Go to Prediction", key="action_new", use_container_width=True):
                st.query_params.page = "prediction"
                st.rerun()
        
        with col2:
            st.markdown("""
                <div class="action-card">
                    <h3>Risk Analysis Report</h3>
                </div>
            """, unsafe_allow_html=True)
            if st.button("View Reports", key="action_report", use_container_width=True):
                st.query_params.page = "reports"
                st.rerun()
        
        with col3:
            st.markdown("""
                <div class="action-card">
                    <h3>Schedule Follow-up</h3>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Go to Appointments", key="action_appt", use_container_width=True):
                st.query_params.page = "lab_tech"
                st.rerun()
        
        # High-Priority Cases
        st.markdown("---")
        st.markdown("## High-Priority Cases")
        
        high_risk_recent = [p for p in all_predictions[:20] if p.risk_level == "High"]
        
        if high_risk_recent:
            for pred in high_risk_recent:
                patient = patient_service.get_patient_by_id(pred.patient_id)
                
                if patient:
                    with st.expander(f"URGENT: {patient.name} - {pred.risk_level} Risk"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**MRN:** {patient.mrn}")
                            st.write(f"**Age:** {patient.age}")
                            st.write(f"**Gender:** {patient.gender}")
                        with col2:
                            st.write(f"**Risk Level:** {pred.risk_level}")
                            st.write(f"**Confidence:** {pred.confidence:.1%}")
                            st.write(f"**Test Date:** {pred.created_at.strftime('%Y-%m-%d %H:%M')}")
                        
                        if st.button(f"Schedule Appointment", key=f"sched_{pred.id}"):
                            st.query_params.page = "lab_tech"
                            st.rerun()
        else:
            st.success("No high-risk cases currently!")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
        st.info("Make sure database is connected")
