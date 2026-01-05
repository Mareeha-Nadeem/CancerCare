"""
Appointments - Modern Design
Manage patient appointments
"""
import streamlit as st
from datetime import datetime


def show():
    """Modern appointments page"""
    
    st.markdown("""
        <style>
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="page-header">
            <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                Appointments
            </h1>
            <p style="color: #64748B; margin-top: 8px;">Schedule and manage patient appointments</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("📅 Appointment scheduling system")
    
    with st.form("schedule_appointment"):
        col1, col2 = st.columns(2)
        with col1:
            appt_date = st.date_input("Date")
            appt_time = st.time_input("Time")
        with col2:
            patient_name = st.text_input("Patient Name")
            appt_type = st.selectbox("Type", ["Consultation", "Follow-up", "Screening"])
        
        if st.form_submit_button("📅 Schedule", use_container_width=True):
            st.success("✅ Appointment scheduled!")
