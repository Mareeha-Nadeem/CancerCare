"""
CancerCare - Patients Management Page
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service
from datetime import datetime
import json

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .page-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #00d9ff;
            margin-bottom: 2rem;
        }
        
        .page-title {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #00d9ff;
            text-align: center;
            margin: 1rem 0;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            color: #b0b0b0;
            font-size: 1rem;
            margin-top: 0.5rem;
        }
        
        .patient-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #00d9ff;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .patient-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">👥 Patient Management</h1>
            <p style="color: #b0b0b0;">Manage patient records and view prediction history</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 All Patients", "➕ Add Patient", "🔍 Search Patient"])
    
    with tab1:
        st.subheader("All Patients")
        
        try:
            patients = patient_service.get_all_patients(limit=100)
            
            if patients:
                # Statistics
                total_patients = patient_service.get_patient_count()
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-number">{total_patients}</div>
                            <div class="stat-label">Total Patients</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    male_count = sum(1 for p in patients if p.gender in ['M', 'Male'])
                    st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-number">{male_count}</div>
                            <div class="stat-label">Male</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    female_count = sum(1 for p in patients if p.gender in ['F', 'Female'])
                    st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-number">{female_count}</div>
                            <div class="stat-label">Female</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    avg_age = sum(p.age for p in patients) / len(patients)
                    st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-number">{avg_age:.0f}</div>
                            <div class="stat-label">Avg Age</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Patient list
                for patient in patients:
                    with st.expander(f"👤 {patient.name} (MRN: {patient.mrn})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Age:** {patient.age}")
                            st.write(f"**Gender:** {patient.gender}")
                            st.write(f"**Contact:** {patient.contact or 'N/A'}")
                            st.write(f"**Email:** {patient.email or 'N/A'}")
                        
                        with col2:
                            st.write(f"**Patient ID:** {patient.id}")
                            st.write(f"**Created:** {patient.created_at.strftime('%Y-%m-%d')}")
                        
                        # Get predictions
                        predictions = prediction_service.get_patient_predictions(patient.id)
                        
                        if predictions:
                            st.write(f"**Predictions:** {len(predictions)}")
                            latest = predictions[0]
                            probs = json.loads(latest.probabilities)
                            
                            risk_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                            st.write(f"**Latest Risk:** {risk_color.get(latest.risk_level, '⚪')} {latest.risk_level} ({latest.confidence:.1%} confidence)")
                        else:
                            st.write("**Predictions:** None")
                        
                        st.markdown("---")
                        
                        # Edit and Delete buttons
                        col_edit, col_delete = st.columns(2)
                        
                        with col_edit:
                            if st.button(f"✏️ Edit", key=f"edit_{patient.id}"):
                                st.session_state[f'editing_{patient.id}'] = True
                                st.rerun()
                        
                        with col_delete:
                            if st.button(f"🗑️ Delete", key=f"delete_{patient.id}", type="secondary"):
                                if st.session_state.get(f'confirm_delete_{patient.id}'):
                                    success, error = patient_service.delete_patient(patient.id)
                                    if success:
                                        st.success(f"✅ Patient {patient.name} deleted!")
                                        st.session_state.pop(f'confirm_delete_{patient.id}', None)
                                        st.rerun()
                                    else:
                                        st.error(f"Error: {error}")
                                else:
                                    st.session_state[f'confirm_delete_{patient.id}'] = True
                                    st.warning("⚠️ Click Delete again to confirm")
                        
                        # Edit form
                        if st.session_state.get(f'editing_{patient.id}'):
                            st.markdown("### Edit Patient Information")
                            with st.form(f"edit_form_{patient.id}"):
                                edit_col1, edit_col2 = st.columns(2)
                                
                                with edit_col1:
                                    edit_name = st.text_input("Name", value=patient.name)
                                    edit_age = st.number_input("Age", min_value=0, max_value=150, value=patient.age)
                                    edit_email = st.text_input("Email", value=patient.email or "")
                                
                                with edit_col2:
                                    edit_mrn = st.text_input("MRN", value=patient.mrn)
                                    edit_gender = st.selectbox("Gender", ["M", "F"], index=0 if patient.gender == "M" else 1)
                                    edit_contact = st.text_input("Contact", value=patient.contact or "")
                                
                                col_save, col_cancel = st.columns(2)
                                
                                with col_save:
                                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                        update_data = {
                                            'name': edit_name,
                                            'age': edit_age,
                                            'gender': edit_gender,
                                            'contact': edit_contact,
                                            'email': edit_email if edit_email else None,
                                            'mrn': edit_mrn
                                        }
                                        
                                        updated_patient, error = patient_service.update_patient(patient.id, update_data)
                                        if error:
                                            st.error(f"Error: {error}")
                                        else:
                                            st.success(f"✅ Patient updated successfully!")
                                            st.session_state.pop(f'editing_{patient.id}', None)
                                            st.rerun()
                                
                                with col_cancel:
                                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                                        st.session_state.pop(f'editing_{patient.id}', None)
                                        st.rerun()
            else:
                st.info("No patients found. Add a patient to get started!")
                
        except Exception as e:
            st.error(f"Error loading patients: {e}")
    
    with tab2:
        st.subheader("Add New Patient")
        
        with st.form("add_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                mrn = st.text_input("MRN*", help="Medical Record Number (unique)")
                name = st.text_input("Full Name*")
                age = st.number_input("Age*", min_value=0, max_value=150, value=50)
                email = st.text_input("Email", placeholder="patient@example.com", help="Email for notifications")
            
            with col2:
                gender = st.selectbox("Gender*", ["M", "F"])
                contact = st.text_input("Contact Number")
            
            submit = st.form_submit_button("Add Patient", use_container_width=True)
            
            if submit:
                if not mrn or not name:
                    st.error("Please fill in all required fields (marked with *)")
                else:
                    patient_data = {
                        'mrn': mrn,
                        'name': name,
                        'age': age,
                        'gender': gender,
                        'contact': contact,
                        'email': email if email else None
                    }
                    
                    patient, error = patient_service.create_patient(patient_data)
                    
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.success(f"✅ Patient {name} added successfully!")
                        if email:
                            st.info(f"📧 Notifications will be sent to {email}")
                        st.balloons()
    
    with tab3:
        st.subheader("Search Patient")
        
        search_query = st.text_input("🔍 Search by Name or MRN")
        
        if search_query:
            try:
                results = patient_service.search_patients(search_query)
                
                if results:
                    st.write(f"Found {len(results)} patient(s)")
                    
                    for patient in results:
                        st.markdown(f"""
                            <div class="patient-card">
                                <h3 style="color: #00d9ff;">{patient.name}</h3>
                                <p><strong>MRN:</strong> {patient.mrn} | <strong>Age:</strong> {patient.age} | <strong>Gender:</strong> {patient.gender}</p>
                                <p><strong>Contact:</strong> {patient.contact or 'N/A'}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No patients found matching your search.")
            except Exception as e:
                st.error(f"Search error: {e}")
    
    # Back button
    st.markdown("---")
    if st.button("⬅️ Back to Home"):
        st.query_params.page = "home"
        st.rerun()
