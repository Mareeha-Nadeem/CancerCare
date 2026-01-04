"""
CancerCare - Advanced Analytics Dashboard
Comprehensive data visualization and statistics
"""
import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service
from core.services.doctor_service import doctor_service
from core.services.appointment_service import appointment_service
from core.network_logger import network_logger
from core.network_monitor import network_monitor
import json

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .dashboard-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #00d9ff;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.3);
        }
        
        .dashboard-title {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #00d9ff;
            text-align: center;
            margin: 0.5rem 0;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-label {
            color: #b0b0b0;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        
        .chart-container {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #00d9ff;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="dashboard-header">
            <h1 class="dashboard-title"> Analytics Dashboard</h1>
            <p style="color: #b0b0b0;">Real-time insights and data visualization</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Refresh button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button(" Refresh Data"):
            st.rerun()
    
    try:
        # Get all data
        patients = patient_service.get_all_patients(limit=1000)
        predictions = prediction_service.get_all_predictions(limit=1000)
        doctors = doctor_service.get_all_doctors()
        appointment_stats = appointment_service.get_appointment_stats()
        risk_dist = prediction_service.get_risk_distribution()
        network_stats = network_logger.get_statistics()
        system_metrics = network_monitor.get_system_metrics()
        
        # Key Metrics Row
        st.markdown("##  Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(patients)}</div>
                    <div class="metric-label">Total Patients</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(predictions)}</div>
                    <div class="metric-label">Predictions Made</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(doctors)}</div>
                    <div class="metric-label">Doctors</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{appointment_stats['total']}</div>
                    <div class="metric-label">Appointments</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Two column layout
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Risk Distribution Pie Chart
            st.markdown("###  Risk Distribution")
            
            if risk_dist['total'] > 0:
                fig_risk = go.Figure(data=[go.Pie(
                    labels=list(risk_dist['counts'].keys()),
                    values=list(risk_dist['counts'].values()),
                    marker=dict(colors=['#00ff88', '#ffbe0b', '#ff006e']),
                    hole=0.4,
                    textinfo='label+percent',
                    textfont=dict(color='white', size=14)
                )])
                
                fig_risk.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    showlegend=True,
                    height=350
                )
                
                st.plotly_chart(fig_risk, use_container_width=True)
            else:
                st.info("No predictions yet")
            
            # Patient Age Distribution
            st.markdown("###  Patient Age Distribution")
            
            if patients:
                ages = [p.age for p in patients]
                
                fig_age = go.Figure(data=[go.Histogram(
                    x=ages,
                    nbinsx=20,
                    marker=dict(
                        color='#00d9ff',
                        line=dict(color='#ff006e', width=1)
                    )
                )])
                
                fig_age.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    xaxis=dict(title="Age", gridcolor='rgba(0, 217, 255, 0.2)'),
                    yaxis=dict(title="Count", gridcolor='rgba(0, 217, 255, 0.2)'),
                    height=350
                )
                
                st.plotly_chart(fig_age, use_container_width=True)
        
        with col_right:
            # Appointment Status
            st.markdown("###  Appointment Status")
            
            fig_appointments = go.Figure(data=[go.Bar(
                x=['Scheduled', 'Completed', 'Cancelled'],
                y=[
                    appointment_stats['scheduled'],
                    appointment_stats['completed'],
                    appointment_stats['cancelled']
                ],
                marker=dict(
                    color=['#ffbe0b', '#00ff88', '#ff006e'],
                    line=dict(color='#00d9ff', width=2)
                ),
                text=[
                    appointment_stats['scheduled'],
                    appointment_stats['completed'],
                    appointment_stats['cancelled']
                ],
                textposition='auto'
            )])
            
            fig_appointments.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(title="Status", gridcolor='rgba(0, 217, 255, 0.2)'),
                yaxis=dict(title="Count", gridcolor='rgba(0, 217, 255, 0.2)'),
                height=350
            )
            
            st.plotly_chart(fig_appointments, use_container_width=True)
            
            # Gender Distribution
            st.markdown("###  Gender Distribution")
            
            if patients:
                male_count = sum(1 for p in patients if p.gender in ['M', 'Male'])
                female_count = sum(1 for p in patients if p.gender in ['F', 'Female'])
                
                fig_gender = go.Figure(data=[go.Bar(
                    x=['Male', 'Female'],
                    y=[male_count, female_count],
                    marker=dict(
                        color=['#00d9ff', '#ff006e'],
                        line=dict(color='white', width=2)
                    ),
                    text=[male_count, female_count],
                    textposition='auto'
                )])
                
                fig_gender.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    xaxis=dict(title="Gender", gridcolor='rgba(0, 217, 255, 0.2)'),
                    yaxis=dict(title="Count", gridcolor='rgba(0, 217, 255, 0.2)'),
                    height=350
                )
                
                st.plotly_chart(fig_gender, use_container_width=True)
        
        # Network Statistics Section
        st.markdown("---")
        st.markdown("##  Network Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Requests", network_stats['total_requests'])
        
        with col2:
            st.metric("Avg Response Time", f"{network_stats['avg_response_time_ms']:.2f} ms")
        
        with col3:
            st.metric("Data Sent", f"{network_stats['total_data_sent_mb']:.2f} MB")
        
        with col4:
            st.metric("CPU Usage", f"{system_metrics['cpu_percent']:.1f}%")
        
        # Recent Predictions Table
        if predictions:
            st.markdown("---")
            st.markdown("##  Recent Predictions")
            
            # Create DataFrame
            recent_predictions = []
            for pred in predictions[:10]:
                probs = json.loads(pred.probabilities)
                recent_predictions.append({
                    'ID': pred.id,
                    'Patient ID': pred.patient_id,
                    'Risk Level': pred.risk_level,
                    'Confidence': f"{pred.confidence:.1%}",
                    'Date': pred.created_at.strftime('%Y-%m-%d %H:%M')
                })
            
            df = pd.DataFrame(recent_predictions)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Statistics Summary
        st.markdown("---")
        st.markdown("##  Summary Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Patient Statistics")
            if patients:
                avg_age = sum(p.age for p in patients) / len(patients)
                st.write(f"**Average Age:** {avg_age:.1f} years")
                st.write(f"**Total Patients:** {len(patients)}")
                st.write(f"**Male Patients:** {male_count}")
                st.write(f"**Female Patients:** {female_count}")
        
        with col2:
            st.markdown("### Prediction Statistics")
            if risk_dist['total'] > 0:
                st.write(f"**Total Predictions:** {risk_dist['total']}")
                st.write(f"**High Risk:** {risk_dist['counts']['High']} ({risk_dist['percentages']['High']}%)")
                st.write(f"**Medium Risk:** {risk_dist['counts']['Medium']} ({risk_dist['percentages']['Medium']}%)")
                st.write(f"**Low Risk:** {risk_dist['counts']['Low']} ({risk_dist['percentages']['Low']}%)")
    
    except Exception as e:
        st.error(f"Error loading dashboard data: {e}")
        st.info("Make sure the database is connected and tables are initialized.")
    
    # Back button
    st.markdown("---")
    if st.button(" Back to Home"):
        st.query_params.page = "home"
        st.rerun()
