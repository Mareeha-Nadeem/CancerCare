"""
CancerCare - Doctors Portal Page
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.doctor_service import doctor_service
from core.services.appointment_service import appointment_service
from core.network_monitor import network_monitor
import plotly.graph_objects as go

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
        
        .doctor-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #00d9ff;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .doctor-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.4);
        }
        
        .stat-card {
            background: linear-gradient(135deg, #ff006e 0%, #ffbe0b 100%);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            color: white;
            margin: 1rem 0;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 900;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">👨‍⚕️ Doctors Portal</h1>
            <p style="color: #b0b0b0;">Manage doctors and appointments</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👨‍⚕️ Doctors", "➕ Add Doctor", "📅 Appointments", "📊 Network Stats"])
    
    with tab1:
        st.subheader("All Doctors")
        
        try:
            doctors = doctor_service.get_all_doctors()
            
            if doctors:
                st.write(f"**Total Doctors:** {len(doctors)}")
                
                for doctor in doctors:
                    with st.expander(f"👨‍⚕️ {doctor.name} - {doctor.specialization}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Name:** {doctor.name}")
                            st.write(f"**Specialization:** {doctor.specialization or 'General'}")
                        
                        with col2:
                            st.write(f"**Email:** {doctor.email}")
                            st.write(f"**Phone:** {doctor.phone or 'N/A'}")
                        
                        st.write(f"**Member since:** {doctor.created_at.strftime('%Y-%m-%d')}")
                        
                        st.markdown("---")
                        
                        # Edit and Delete buttons
                        col_edit, col_delete = st.columns(2)
                        
                        with col_edit:
                            if st.button(f"✏️ Edit", key=f"edit_doctor_{doctor.id}"):
                                st.session_state[f'editing_doctor_{doctor.id}'] = True
                                st.rerun()
                        
                        with col_delete:
                            if st.button(f"🗑️ Delete", key=f"delete_doctor_{doctor.id}", type="secondary"):
                                if st.session_state.get(f'confirm_delete_doctor_{doctor.id}'):
                                    success, error = doctor_service.delete_doctor(doctor.id)
                                    if success:
                                        st.success(f"✅ Doctor {doctor.name} deleted!")
                                        st.session_state.pop(f'confirm_delete_doctor_{doctor.id}', None)
                                        st.rerun()
                                    else:
                                        st.error(f"Error: {error}")
                                else:
                                    st.session_state[f'confirm_delete_doctor_{doctor.id}'] = True
                                    st.warning("⚠️ Click Delete again to confirm")
                        
                        # Edit form
                        if st.session_state.get(f'editing_doctor_{doctor.id}'):
                            st.markdown("### Edit Doctor Information")
                            with st.form(f"edit_doctor_form_{doctor.id}"):
                                edit_name = st.text_input("Name", value=doctor.name)
                                edit_email = st.text_input("Email", value=doctor.email)
                                edit_specialization = st.selectbox(
                                    "Specialization",
                                    ["Oncology", "Pulmonology", "Radiology", "General Medicine", "Surgery"],
                                    index=["Oncology", "Pulmonology", "Radiology", "General Medicine", "Surgery"].index(doctor.specialization) if doctor.specialization in ["Oncology", "Pulmonology", "Radiology", "General Medicine", "Surgery"] else 0
                                )
                                edit_phone = st.text_input("Phone", value=doctor.phone or "")
                                
                                col_save, col_cancel = st.columns(2)
                                
                                with col_save:
                                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                        update_data = {
                                            'name': edit_name,
                                            'email': edit_email,
                                            'specialization': edit_specialization,
                                            'phone': edit_phone if edit_phone else None
                                        }
                                        
                                        updated_doctor, error = doctor_service.update_doctor(doctor.id, update_data)
                                        if error:
                                            st.error(f"Error: {error}")
                                        else:
                                            st.success(f"✅ Doctor updated successfully!")
                                            st.session_state.pop(f'editing_doctor_{doctor.id}', None)
                                            st.rerun()
                                
                                with col_cancel:
                                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                                        st.session_state.pop(f'editing_doctor_{doctor.id}', None)
                                        st.rerun()
            else:
                st.info("No doctors registered. Add a doctor to get started!")
                
        except Exception as e:
            st.error(f"Error loading doctors: {e}")
    
    with tab2:
        st.subheader("Register New Doctor")
        
        with st.form("add_doctor_form"):
            name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            specialization = st.selectbox(
                "Specialization",
                ["Oncology", "Pulmonology", "Radiology", "General Medicine", "Surgery"]
            )
            phone = st.text_input("Phone Number")
            
            submit = st.form_submit_button("Register Doctor", use_container_width=True)
            
            if submit:
                if not name or not email:
                    st.error("Please fill in all required fields")
                else:
                    doctor_data = {
                        'name': name,
                        'email': email,
                        'specialization': specialization,
                        'phone': phone
                    }
                    
                    doctor, error = doctor_service.create_doctor(doctor_data)
                    
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.success(f"✅ Doctor {name} registered successfully!")
                        st.balloons()
    
    with tab3:
        st.subheader("Appointments Dashboard")
        
        try:
            stats = appointment_service.get_appointment_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{stats['total']}</div>
                        <div>Total</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{stats['scheduled']}</div>
                        <div>Scheduled</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{stats['completed']}</div>
                        <div>Completed</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{stats['cancelled']}</div>
                        <div>Cancelled</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Upcoming appointments
            st.markdown("---")
            st.subheader("📅 Upcoming Appointments")
            
            upcoming = appointment_service.get_upcoming_appointments(10)
            
            if upcoming:
                for apt in upcoming:
                    priority_emoji = "🔴" if apt.priority >= 4 else "🟡" if apt.priority >= 2 else "🟢"
                    st.write(f"{priority_emoji} **{apt.appointment_date.strftime('%Y-%m-%d %H:%M')}** - Priority: {apt.priority}")
            else:
                st.info("No upcoming appointments")
                
        except Exception as e:
            st.error(f"Error loading appointments: {e}")
    
    with tab4:
        st.subheader("📊 Network Statistics (Computer Networks Feature)")
        
        try:
            from core.network_logger import network_logger
            
            stats = network_logger.get_statistics()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Requests", stats['total_requests'])
                st.metric("Total Responses", stats['total_responses'])
            
            with col2:
                st.metric("Avg Response Time", f"{stats['avg_response_time_ms']:.2f} ms")
                st.metric("Data Sent", f"{stats['total_data_sent_mb']:.2f} MB")
            
            with col3:
                st.metric("Data Received", f"{stats['total_data_received_mb']:.2f} MB")
            
            # Status code distribution
            if stats['status_code_distribution']:
                st.subheader("Status Code Distribution")
                
                codes = list(stats['status_code_distribution'].keys())
                counts = list(stats['status_code_distribution'].values())
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=[str(c) for c in codes],
                        y=counts,
                        marker=dict(
                            color=['#00ff88' if c == 200 else '#ff006e' for c in codes],
                            line=dict(color='#00d9ff', width=2)
                        )
                    )
                ])
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    xaxis=dict(title="Status Code", color='#e0e0e0'),
                    yaxis=dict(title="Count", color='#e0e0e0'),
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # System metrics
            st.subheader("🖥️ System Metrics")
            system_metrics = network_monitor.get_system_metrics()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("CPU Usage", f"{system_metrics['cpu_percent']:.1f}%")
                st.metric("Memory Usage", f"{system_metrics['memory_percent']:.1f}%")
            
            with col2:
                st.metric("Network Bytes Sent", f"{system_metrics['network_bytes_sent'] / (1024*1024):.2f} MB")
                st.metric("Network Bytes Received", f"{system_metrics['network_bytes_recv'] / (1024*1024):.2f} MB")
            
        except Exception as e:
            st.warning(f"Network monitoring unavailable: {e}")
    
    # Back button
    st.markdown("---")
    if st.button("⬅️ Back to Home"):
        st.query_params.page = "home"
        st.rerun()
