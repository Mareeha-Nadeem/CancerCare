"""
Patient History Tracker - Complete medical timeline
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service
from core.services.appointment_service import appointment_service
import json

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .history-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #00d9ff;
            margin-bottom: 2rem;
        }
        
        .timeline-event {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #00d9ff;
            margin: 1rem 0;
            position: relative;
        }
        
        .timeline-date {
            color: #ffbe0b;
            font-weight: 700;
            font-size: 1.1rem;
        }
        
        .risk-badge {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 700;
            display: inline-block;
            margin: 0.5rem 0;
        }
        
        .risk-high {
            background: #ff006e;
            color: white;
        }
        
        .risk-medium {
            background: #ffbe0b;
            color: black;
        }
        
        .risk-low {
            background: #00ff88;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="history-header"><h1 style="color: #00d9ff;">📜 Patient History Tracker</h1></div>', unsafe_allow_html=True)
    
    # Patient selection
    patients = patient_service.get_all_patients(limit=1000)
    
    if not patients:
        st.warning("No patients in database. Please add patients first.")
        if st.button("➕ Add Patient"):
            st.query_params.page = "patients"
            st.rerun()
        return
    
    patient_options = {f"{p.name} (MRN: {p.mrn})": p for p in patients}
    selected_patient_name = st.selectbox("Select Patient", list(patient_options.keys()))
    patient = patient_options[selected_patient_name]
    
    # Patient info card
    st.markdown("## 👤 Patient Information")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Name", patient.name)
    with col2:
        st.metric("Age", patient.age)
    with col3:
        st.metric("Gender", patient.gender)
    with col4:
        st.metric("MRN", patient.mrn)
    
    st.markdown("---")
    
    # Get all patient data
    predictions = prediction_service.get_patient_predictions(patient.id)
    appointments = appointment_service.get_patient_appointments(patient.id)
    
    # Statistics
    st.markdown("## 📊 Patient Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Tests", len(predictions))
    
    with col2:
        if predictions:
            latest_risk = predictions[0].risk_level
            st.metric("Latest Risk", latest_risk)
        else:
            st.metric("Latest Risk", "N/A")
    
    with col3:
        st.metric("Appointments", len(appointments))
    
    # Risk trend chart
    if predictions and len(predictions) > 1:
        st.markdown("---")
        st.markdown("## 📈 Risk Trend Over Time")
        
        # Map risk levels to numbers for plotting
        risk_map = {'Low': 1, 'Medium': 2, 'High': 3}
        
        dates = [p.created_at for p in reversed(predictions)]
        risks = [risk_map[p.risk_level] for p in reversed(predictions)]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=risks,
            mode='lines+markers',
            line=dict(color='#00d9ff', width=3),
            marker=dict(size=10, color='#ff006e'),
            fill='tozeroy',
            fillcolor='rgba(0, 217, 255, 0.2)'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            xaxis=dict(title="Date", gridcolor='rgba(0, 217, 255, 0.2)'),
            yaxis=dict(
                title="Risk Level",
                gridcolor='rgba(0, 217, 255, 0.2)',
                tickmode='array',
                tickvals=[1, 2, 3],
                ticktext=['Low', 'Medium', 'High']
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Complete Timeline
    st.markdown("---")
    st.markdown("## 🕐 Complete Medical Timeline")
    
    # Combine predictions and appointments into timeline
    timeline = []
    
    for pred in predictions:
        probs = json.loads(pred.probabilities)
        timeline.append({
            'date': pred.created_at,
            'type': 'Prediction',
            'icon': '🔬',
            'title': f"Risk Assessment: {pred.risk_level}",
            'details': f"Confidence: {pred.confidence:.1%}<br>Probabilities: Low {probs.get('Low', 0):.1%}, Medium {probs.get('Medium', 0):.1%}, High {probs.get('High', 0):.1%}",
            'risk': pred.risk_level
        })
    
    for apt in appointments:
        timeline.append({
            'date': apt.created_at,
            'type': 'Appointment',
            'icon': '📅',
            'title': f"Appointment Scheduled",
            'details': f"Date: {apt.appointment_date.strftime('%Y-%m-%d %H:%M')}<br>Status: {apt.status}<br>Priority: {apt.priority}",
            'risk': 'Low'  # Default for appointments
        })
    
    # Sort by date (newest first)
    timeline.sort(key=lambda x: x['date'], reverse=True)
    
    if timeline:
        for event in timeline:
            risk_class = f"risk-{event['risk'].lower()}"
            
            st.markdown(f"""
                <div class="timeline-event">
                    <div class="timeline-date">{event['icon']} {event['date'].strftime('%Y-%m-%d %H:%M')}</div>
                    <h3 style="color: #00d9ff; margin-top: 0.5rem;">{event['title']}</h3>
                    <p>{event['details']}</p>
                    <span class="risk-badge {risk_class}">{event['type']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No medical history recorded yet for this patient.")
    
    # Export options
    st.markdown("---")
    st.markdown("## 📥 Export Patient Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            st.info("PDF generation feature - coming soon!")
    
    with col2:
        if st.button("📊 Export to CSV", use_container_width=True):
            import pandas as pd
            
            # Create CSV data
            data = []
            for pred in predictions:
                data.append({
                    'Date': pred.created_at.strftime('%Y-%m-%d %H:%M'),
                    'Risk Level': pred.risk_level,
                    'Confidence': pred.confidence
                })
            
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            
            st.download_button(
                "💾 Download CSV",
                csv,
                f"patient_{patient.mrn}_history.csv",
                "text/csv"
            )
    
    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("Email feature - configure SMTP settings first!")
    
    # Back button
    st.markdown("---")
    if st.button("⬅️ Back to Lab Dashboard"):
        st.query_params.page = "lab_dashboard"
        st.rerun()
