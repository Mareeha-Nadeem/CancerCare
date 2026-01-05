"""
Patient Management - Modern Clean Design
Efficient patient list with search and quick actions
"""
import streamlit as st
from core.services.patient_service import patient_service


def show():
    """Display modern patient management page"""
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;
        }
        
        .page-header {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(16px);
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 32px;
        }
        
        .patient-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
            border: 1px solid #E2E8F0;
            transition: all 0.2s ease;
        }
        
        .patient-card:hover {
            border-color: #14B8A6;
            box-shadow: 0 4px 12px rgba(20, 184, 166, 0.15);
        }
        
        .patient-name {
            font-size: 18px;
            font-weight: 700;
            color: #1F2937;
        }
        
        .patient-info {
            font-size: 14px;
            color: #64748B;
            margin-top: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="page-header">
            <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                Patient Management
            </h1>
            <p style="color: #64748B; margin-top: 8px;">View and manage patient records</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search patients", placeholder="Search by name or MRN...")
    with col2:
        if st.button("➕ Add Patient", use_container_width=True):
            st.session_state.show_add_form = True
    
    # Get patients
    patients = patient_service.get_all_patients()
    
    # Filter by search
    if search:
        patients = [p for p in patients if search.lower() in p.name.lower() or 
                   (p.mrn and search.lower() in p.mrn.lower())]
    
    # Display count
    st.markdown(f"<p style='color: #64748B; margin: 16px 0;'>**{len(patients)} patients** found</p>", 
                unsafe_allow_html=True)
    
    # Patient list
    if patients:
        for patient in patients:
            st.markdown(f"""
                <div class="patient-card">
                    <div class="patient-name">{patient.name}</div>
                    <div class="patient-info">
                        MRN: {patient.mrn or 'N/A'} | Age: {patient.age} | Gender: {patient.gender}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No patients found")
    
    # Add patient form
    if st.session_state.get('show_add_form'):
        with st.form("add_patient"):
            st.subheader("Add New Patient")
            name = st.text_input("Name")
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", 1, 120, 50)
                gender = st.selectbox("Gender", ["M", "F"])
            with col2:
                mrn = st.text_input("MRN (optional)")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save", use_container_width=True):
                    patient_data = {'name': name, 'age': age, 'gender': gender, 'mrn': mrn}
                    patient, error = patient_service.create_patient(patient_data)
                    if error:
                        st.error(error)
                    else:
                        st.session_state.show_add_form = False
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.show_add_form = False
                    st.rerun()
