"""
Lab Dashboard - Modern & Efficient Design
Clean KPI cards, smart layout, professional medical theme
"""
import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta
import plotly.graph_objects as go

from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service


def show():
    """Display ultra-modern efficient dashboard"""
    
    # Premium dashboard CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Dashboard Header */
        .dashboard-header {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(16px);
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 32px;
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .dash-title {
            font-size: 36px;
            font-weight: 800;
            background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        
        .dash-subtitle {
            color: #64748B;
            font-size: 16px;
            margin-top: 8px;
        }
        
        /* Efficient KPI Card */
        .kpi-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(20, 184, 166, 0.1);
            transition: all 0.3s ease;
        }
        
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(20, 184, 166, 0.15);
            border-color: rgba(20, 184, 166, 0.3);
        }
        
        .kpi-label {
            font-size: 13px;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }
        
        .kpi-value {
            font-size: 36px;
            font-weight: 800;
            color: #14B8A6;
            margin: 8px 0;
        }
        
        .kpi-change {
            font-size: 14px;
            font-weight: 600;
            color: #10B981;
        }
        
        /* Quick Action Card */
        .action-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            border: 2px solid #E2E8F0;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .action-card:hover {
            border-color: #14B8A6;
            box-shadow: 0 4px 12px rgba(20, 184, 166, 0.15);
        }
        
        .action-icon {
            font-size: 32px;
            margin-bottom: 12px;
        }
        
        .action-title {
            font-size: 16px;
            font-weight: 600;
            color: #1F2937;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Logout button
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "landing"
            st.rerun()
    
    # Dashboard Header
    st.markdown("""
        <div class="dashboard-header">
            <h1 class="dash-title">Lab Dashboard</h1>
            <p class="dash-subtitle">Real-time overview of patient analytics and lab operations</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get data
    all_predictions = prediction_service.get_all_predictions()
    all_patients = patient_service.get_all_patients()
    
    # Calculate stats
    total_predictions = len(all_predictions)
    total_patients = len(all_patients)
    
    high_risk = sum(1 for p in all_predictions if p.risk_level == "High")
    
    # Recent activity
    today = datetime.now().date()
    today_predictions = sum(1 for p in all_predictions 
                           if p.created_at and p.created_at.date() == today)
    
    # KPI Cards
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Patients</div>
                <div class="kpi-value">{total_patients}</div>
                <div class="kpi-change">↗ Active Records</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Predictions</div>
                <div class="kpi-value">{total_predictions}</div>
                <div class="kpi-change">↗ All Time</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">High Risk</div>
                <div class="kpi-value" style="color: #EF4444;">{high_risk}</div>
                <div class="kpi-change" style="color: #EF4444;">⚠ Requires Attention</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Today</div>
                <div class="kpi-value">{today_predictions}</div>
                <div class="kpi-change">↗ New Predictions</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("<h2 style='font-size: 24px; font-weight: 700; color: #1F2937; margin-bottom: 24px;'>Quick Actions</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔬 New Analysis", use_container_width=True):
            st.switch_page("pages/prediction.py")
    
    with col2:
        if st.button("👥 View Patients", use_container_width=True):
            st.switch_page("pages/patients.py")
    
    with col3:
        if st.button("📊 Reports", use_container_width=True):
            st.switch_page("pages/reports.py")
    
    with col4:
        if st.button("🏥 Post-Diagnosis", use_container_width=True):
            st.switch_page("pages/post_diagnosis.py")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Recent Activity & Chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h2 style='font-size: 24px; font-weight: 700; color: #1F2937; margin-bottom: 16px;'>Risk Distribution</h2>", unsafe_allow_html=True)
        
        # Risk distribution chart
        risk_counts = {"High": high_risk, 
                      "Medium": sum(1 for p in all_predictions if p.risk_level == "Medium"),
                      "Low": sum(1 for p in all_predictions if p.risk_level == "Low")}
        
        fig = go.Figure(data=[go.Pie(
            labels=list(risk_counts.keys()),
            values=list(risk_counts.values()),
            marker=dict(colors=['#EF4444', '#F59E0B', '#10B981']),
            hole=0.4,
            textinfo='label+percent',
            textfont=dict(size=14, family='Inter')
        )])
        
        fig.update_layout(
            showlegend=True,
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("<h2 style='font-size: 24px; font-weight: 700; color: #1F2937; margin-bottom: 16px;'>Recent Activity</h2>", unsafe_allow_html=True)
        
        # Recent predictions
        recent = sorted(all_predictions, key=lambda x: x.created_at or datetime.min, reverse=True)[:5]
        
        for pred in recent:
            risk_color = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}.get(pred.risk_level, "#64748B")
            st.markdown(f"""
                <div style="background: white; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid {risk_color};">
                    <div style="font-weight: 600; color: #1F2937;">Patient #{pred.patient_id}</div>
                    <div style="font-size: 12px; color: #64748B;">
                        {pred.risk_level} Risk | {pred.created_at.strftime('%b %d, %Y') if pred.created_at else 'N/A'}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        if not recent:
            st.info("No recent predictions")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
