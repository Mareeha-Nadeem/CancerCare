"""
Enhanced Lab Technician Dashboard
Primary interface for lab technicians with comprehensive tools
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service
from core.services.appointment_service import appointment_service
from core.notification_service import notification_service
import json

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .tech-dashboard {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 3px solid #ffbe0b;
            margin-bottom: 2rem;
            box-shadow: 0 15px 40px rgba(255, 190, 11, 0.4);
        }
        
        .tech-title {
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(90deg, #ffbe0b 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        
        .quick-action {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #00d9ff;
            text-align: center;
            margin: 1rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .quick-action:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 217, 255, 0.5);
            border-color: #ffbe0b;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #ff006e 0%, #ffbe0b 100%);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            color: white;
            margin: 1rem 0;
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: 900;
        }
        
        .pending-sample {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #ff006e;
            margin: 1rem 0;
        }
        
        .completed-sample {
            border-left: 5px solid #00ff88;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="tech-dashboard">
            <h1 class="tech-title">🔬 Lab Technician Control Center</h1>
            <p style="color: #b0b0b0; text-align: center; font-size: 1.2rem;">
                Your comprehensive workspace for sample analysis and risk assessment
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick stats row
    st.markdown("## 📊 Today's Overview")
    
    try:
        all_predictions = prediction_service.get_all_predictions(limit=1000)
        today = datetime.now().date()
        today_predictions = [p for p in all_predictions if p.created_at.date() == today]
        
        pending_patients = patient_service.get_all_patients(limit=1000)
        high_risk_today = [p for p in today_predictions if p.risk_level == "High"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{len(today_predictions)}</div>
                    <div>Tests Today</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{len(high_risk_today)}</div>
                    <div>High Risk</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            pending_count = len(pending_patients) - len([p for p in all_predictions])
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{max(0, pending_count)}</div>
                    <div>Pending Samples</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{len(pending_patients)}</div>
                    <div>Total Patients</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("## ⚡ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧪 New Sample Analysis", key="new_analysis", use_container_width=True, type="primary"):
                st.query_params.page = "prediction"
                st.rerun()
        
        with col2:
            if st.button("📊 Risk Analysis Report", key="risk_report", use_container_width=True):
                st.session_state['show_risk_report'] = True
        
        with col3:
            if st.button("📅 Schedule Follow-up", key="schedule", use_container_width=True):
                st.query_params.page = "lab_tech"
                st.rerun()
        
        # Risk Analysis Report Section
        if st.session_state.get('show_risk_report', False):
            st.markdown("---")
            st.markdown("## 📈 Risk Analysis Report")
            
            risk_dist = prediction_service.get_risk_distribution()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk distribution pie chart
                fig_pie = go.Figure(data=[go.Pie(
                    labels=list(risk_dist['counts'].keys()),
                    values=list(risk_dist['counts'].values()),
                    marker=dict(colors=['#00ff88', '#ffbe0b', '#ff006e']),
                    hole=0.5,
                    textinfo='label+percent+value',
                    textfont=dict(color='white', size=16)
                )])
                
                fig_pie.update_layout(
                    title="Risk Distribution",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    height=400
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Statistics
                st.markdown("### 📊 Statistics")
                st.write(f"**Total Assessments:** {risk_dist['total']}")
                st.write("")
                st.write("**Risk Breakdown:**")
                st.success(f"✅ Low Risk: {risk_dist['counts']['Low']} ({risk_dist['percentages']['Low']}%)")
                st.warning(f"⚠️ Medium Risk: {risk_dist['counts']['Medium']} ({risk_dist['percentages']['Medium']}%)")
                st.error(f"🔴 High Risk: {risk_dist['counts']['High']} ({risk_dist['percentages']['High']}%)")
                
                # Quality metrics
                st.markdown("---")
                st.markdown("### 🎯 Lab Quality Metrics")
                
                if all_predictions:
                    avg_confidence = sum(p.confidence for p in all_predictions) / len(all_predictions)
                    st.metric("Average Confidence", f"{avg_confidence:.1%}")
                    
                    # Completion rate
                    completion_rate = (len(all_predictions) / len(pending_patients) * 100) if pending_patients else 0
                    st.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        # Recent High-Risk Cases
        st.markdown("---")
        st.markdown("## 🔴 High-Priority Cases (Requires Immediate Attention)")
        
        high_risk_recent = [p for p in all_predictions[:20] if p.risk_level == "High"]
        
        if high_risk_recent:
            for pred in high_risk_recent:
                patient = patient_service.get_patient_by_id(pred.patient_id)
                
                if patient:
                    with st.container():
                        st.markdown(f"""
                            <div class="pending-sample">
                                <h3 style="color: #ff006e;">🔴 URGENT: {patient.name}</h3>
                                <p><strong>MRN:</strong> {patient.mrn} | <strong>Age:</strong> {patient.age} | <strong>Gender:</strong> {patient.gender}</p>
                                <p><strong>Risk Level:</strong> HIGH ({pred.confidence:.1%} confidence)</p>
                                <p><strong>Test Date:</strong> {pred.created_at.strftime('%Y-%m-%d %H:%M')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button(f"📅 Schedule Urgent Appointment", key=f"urgent_{pred.id}"):
                                st.session_state['selected_patient_id'] = patient.id
                                st.session_state['selected_patient_name'] = patient.name
                                st.session_state['prediction_risk'] = pred.risk_level
                                st.query_params.page = "lab_tech"
                                st.rerun()
                        
                        with col2:
                            if st.button(f"📄 Generate Report", key=f"report_{pred.id}"):
                                st.info("Report generation feature coming soon!")
                        
                        with col3:
                            if st.button(f"📨 Notify Doctor", key=f"notify_{pred.id}"):
                                notification_service.broadcast(
                                    "High-Risk Case Alert",
                                    f"Patient {patient.name} has HIGH risk assessment. Immediate attention required.",
                                    "error"
                                )
                                st.success("✅ Doctor notified!")
        else:
            st.success("✅ No high-risk cases currently. Great work!")
        
        # Today's workflow
        st.markdown("---")
        st.markdown("## 📋 Today's Workflow")
        
        if today_predictions:
            # Create timeline
            timeline_data = []
            for pred in today_predictions:
                patient = patient_service.get_patient_by_id(pred.patient_id)
                if patient:
                    timeline_data.append({
                        'time': pred.created_at.strftime('%H:%M'),
                        'patient': patient.name,
                        'risk': pred.risk_level,
                        'confidence': pred.confidence
                    })
            
            for item in sorted(timeline_data, key=lambda x: x['time'], reverse=True):
                risk_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                st.write(f"{item['time']} - {risk_color[item['risk']]} {item['patient']} - {item['risk']} Risk ({item['confidence']:.1%})")
        else:
            st.info("No tests performed today. Start your first analysis!")
        
        # Performance Chart
        st.markdown("---")
        st.markdown("## 📈 Weekly Performance")
        
        # Get last 7 days data
        daily_counts = {}
        for i in range(7):
            day = today - timedelta(days=i)
            count = len([p for p in all_predictions if p.created_at.date() == day])
            daily_counts[day.strftime('%a')] = count
        
        fig_bar = go.Figure(data=[go.Bar(
            x=list(daily_counts.keys()),
            y=list(daily_counts.values()),
            marker=dict(
                color='#ffbe0b',
                line=dict(color='#ff006e', width=2)
            ),
            text=list(daily_counts.values()),
            textposition='auto'
        )])
        
        fig_bar.update_layout(
            title="Tests Performed (Last 7 Days)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            xaxis=dict(title="Day", gridcolor='rgba(0, 217, 255, 0.2)'),
            yaxis=dict(title="Number of Tests", gridcolor='rgba(0, 217, 255, 0.2)'),
            height=350
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
        st.info("Make sure database is connected. Run: python fix_password.py then python init_db_simple.py")
    
    # Footer with tips
    st.markdown("---")
    with st.expander("💡 Lab Technician Tips & Shortcuts"):
        st.markdown("""
        **Quick Workflow:**
        1. 🧪 Use "New Sample Analysis" for quick predictions
        2. 🔴 Monitor high-risk cases daily
        3. 📅 Schedule follow-ups immediately for high-risk patients
        4. 📊 Review weekly performance to track productivity
        
        **Keyboard Shortcuts:**
        - `Ctrl + R` - Refresh dashboard
        - `N` - New analysis (when in prediction page)
        
        **Best Practices:**
        - Process high-risk cases first
        - Double-check patient information
        - Document all findings
        - Schedule appointments within 24 hours for high-risk
        """)
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Home"):
            st.query_params.page = "home"
            st.rerun()
    with col2:
        if st.button("📊 Full Dashboard"):
            st.query_params.page = "dashboard"
            st.rerun()
