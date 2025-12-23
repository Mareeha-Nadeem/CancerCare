"""
Lab Technician & Appointment Booking Page
Interactive appointment scheduling after predictions
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.patient_service import patient_service
from core.services.doctor_service import doctor_service
from core.services.appointment_service import appointment_service
from core.services.prediction_service import prediction_service
from core.notification_service import notification_service, notify_appointment_booked
import json

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .lab-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #ffbe0b;
            margin-bottom: 2rem;
        }
        
        .lab-title {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #ffbe0b 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .patient-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #ffbe0b;
            margin: 1rem 0;
        }
        
        .high-risk {
            border-left: 4px solid #ff006e;
        }
        
        .medium-risk {
            border-left: 4px solid #ffbe0b;
        }
        
        .low-risk {
            border-left: 4px solid #00ff88;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="lab-header">
            <h1 class="lab-title">🔬 Lab Technician Portal</h1>
            <p style="color: #b0b0b0;">Manage predictions and schedule appointments</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Recent Results", "📅 Book Appointment", "📊 My Activity"])
    
    with tab1:
        st.subheader("Recent Prediction Results")
        
        try:
            predictions = prediction_service.get_all_predictions(limit=20)
            
            if predictions:
                for pred in predictions:
                    patient = patient_service.get_patient_by_id(pred.patient_id)
                    
                    if not patient:
                        continue
                    
                    probs = json.loads(pred.probabilities)
                    
                    risk_class = f"{pred.risk_level.lower()}-risk"
                    
                    with st.expander(f"👤 {patient.name} - {pred.risk_level} Risk ({pred.created_at.strftime('%Y-%m-%d %H:%M')})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Patient:** {patient.name}")
                            st.write(f"**MRN:** {patient.mrn}")
                            st.write(f"**Age:** {patient.age}")
                            st.write(f"**Gender:** {patient.gender}")
                        
                        with col2:
                            st.write(f"**Risk Level:** {pred.risk_level}")
                            st.write(f"**Confidence:** {pred.confidence:.1%}")
                            st.write(f"**Test Date:** {pred.created_at.strftime('%Y-%m-%d')}")
                        
                        st.markdown("---")
                        st.write("**Risk Probabilities:**")
                        st.write(f"- Low: {probs.get('Low', 0):.1%}")
                        st.write(f"- Medium: {probs.get('Medium', 0):.1%}")
                        st.write(f"- High: {probs.get('High', 0):.1%}")
                        
                        # Quick action button
                        if st.button(f"📅 Schedule Appointment for {patient.name}", key=f"appt_{pred.id}"):
                            st.session_state['selected_patient_id'] = patient.id
                            st.session_state['selected_patient_name'] = patient.name
                            st.session_state['prediction_risk'] = pred.risk_level
                            st.success(f"✅ Patient selected! Go to 'Book Appointment' tab")
            else:
                st.info("No recent predictions available")
        
        except Exception as e:
            st.error(f"Error loading predictions: {e}")
    
    with tab2:
        st.subheader("Schedule Appointment")
        
        # Check if patient was selected from tab1
        if 'selected_patient_id' in st.session_state:
            st.success(f"✅ Selected Patient: {st.session_state.get('selected_patient_name')}")
            st.info(f"Risk Level: {st.session_state.get('prediction_risk')}")
        
        with st.form("appointment_form"):
            st.markdown("### Patient Selection")
            
            # Patient selection
            patients = patient_service.get_all_patients(limit=100)
            patient_options = {f"{p.name} (MRN: {p.mrn})": p.id for p in patients}
            
            selected_patient_name = st.selectbox(
                "Select Patient",
                list(patient_options.keys()),
                index=0 if 'selected_patient_name' not in st.session_state else 
                      list(patient_options.keys()).index(
                          next((k for k in patient_options.keys() if st.session_state.get('selected_patient_name') in k), list(patient_options.keys())[0])
                      )
            )
            
            patient_id = patient_options[selected_patient_name]
            
            st.markdown("### Appointment Details")
            
            # Doctor selection
            doctors = doctor_service.get_all_doctors()
            doctor_options = {f"{d.name} - {d.specialization}": d.id for d in doctors}
            
            if not doctors:
                st.warning("⚠️ No doctors available. Please add doctors first.")
                selected_doctor = None
            else:
                selected_doctor_name = st.selectbox("Select Doctor", list(doctor_options.keys()))
                selected_doctor = doctor_options[selected_doctor_name]
            
            # Date and time
            col1, col2 = st.columns(2)
            
            with col1:
                appointment_date = st.date_input(
                    "Appointment Date",
                    min_value=datetime.now().date(),
                    value=datetime.now().date() + timedelta(days=1)
                )
            
            with col2:
                appointment_time = st.time_input("Appointment Time", value=datetime.now().time())
            
            # Priority (based on risk)
            priority = st.slider("Priority (1=Low, 5=Urgent)", 1, 5, 3)
            
            # Reason
            reason = st.text_area("Reason for Appointment", 
                                 value="Follow-up consultation for lung cancer risk assessment")
            
            # Notes
            notes = st.text_area("Additional Notes (Optional)")
            
            # Submit button
            submit = st.form_submit_button("📅 Schedule Appointment", use_container_width=True)
            
            if submit:
                if not selected_doctor:
                    st.error("Please select a doctor")
                else:
                    try:
                        appointment_datetime = datetime.combine(appointment_date, appointment_time)
                        
                        appointment_data = {
                            'patient_id': patient_id,
                            'doctor_id': selected_doctor,
                            'appointment_date': appointment_datetime,
                            'reason': reason,
                            'priority': priority,
                            'notes': notes,
                            'status': 'scheduled'
                        }
                        
                        appointment, error = appointment_service.create_appointment(appointment_data)
                        
                        if error:
                            st.error(f"Error: {error}")
                        else:
                            patient = patient_service.get_patient_by_id(patient_id)
                            doctor = doctor_service.get_doctor_by_id(selected_doctor)
                            
                            st.success(f"✅ Appointment scheduled successfully!")
                            st.balloons()
                            
                            # Send notification
                            notify_appointment_booked(
                                patient.name,
                                doctor.name,
                                appointment_datetime.strftime('%Y-%m-%d %H:%M')
                            )
                            
                            # Send email if patient has email
                            if patient.email:
                                try:
                                    from core.email_service import email_service
                                    
                                    email_service.send_appointment_notification(
                                        patient_email=patient.email,
                                        patient_name=patient.name,
                                        doctor_name=doctor.name,
                                        appointment_date=appointment_datetime.strftime('%Y-%m-%d %H:%M'),
                                        reason=reason
                                    )
                                    st.success(f"📧 Appointment confirmation sent to {patient.email}")
                                except Exception as e:
                                    st.warning(f"Appointment saved but email failed: {e}")
                            
                            # Clear selection
                            if 'selected_patient_id' in st.session_state:
                                del st.session_state['selected_patient_id']
                                del st.session_state['selected_patient_name']
                                del st.session_state['prediction_risk']
                            
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error scheduling appointment: {e}")
    
    with tab3:
        st.subheader("Activity Summary")
        
        try:
            stats = appointment_service.get_appointment_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Appointments", stats['total'])
            
            with col2:
                st.metric("Scheduled", stats['scheduled'])
            
            with col3:
                st.metric("Completed", stats['completed'])
            
            with col4:
                st.metric("Cancelled", stats['cancelled'])
            
            # Recent appointments
            st.markdown("---")
            st.markdown("### Recent Appointments")
            
            recent = appointment_service.get_upcoming_appointments(20)
            
            if recent:
                for apt in recent:
                    patient = patient_service.get_patient_by_id(apt.patient_id)
                    doctor = doctor_service.get_doctor_by_id(apt.doctor_id)
                    
                    priority_emoji = "🔴" if apt.priority >= 4 else "🟡" if apt.priority >= 2 else "🟢"
                    
                    st.write(f"{priority_emoji} **{patient.name}** with **Dr. {doctor.name}**")
                    st.write(f"   📅 {apt.appointment_date.strftime('%Y-%m-%d %H:%M')} | Status: {apt.status}")
                    st.write(f"   Reason: {apt.reason}")
                    st.markdown("---")
            else:
                st.info("No recent appointments")
        
        except Exception as e:
            st.error(f"Error loading activity: {e}")
    
    # Back button
    st.markdown("---")
    if st.button("⬅️ Back to Home"):
        st.query_params.page = "home"
        st.rerun()
