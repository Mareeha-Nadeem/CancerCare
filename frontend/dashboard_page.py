"""
Analytics Dashboard - Comprehensive Visual Analytics
"""
import streamlit as st
from core.services.prediction_service import prediction_service
from core.services.patient_service import patient_service
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta


def show():
    """Comprehensive analytics with multiple charts"""
    
    st.markdown("""
        <style>
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        .metric-card {
            background: var(--bg-surface-elevated); border-radius: 12px; padding: 20px; text-align: center;
            border: 1px solid #E2E8F0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="page-header">
            <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                Analytics Dashboard
            </h1>
            <p style="color: var(--text-muted); margin-top: 8px;">Comprehensive visual analytics and insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get data
    predictions = prediction_service.get_all_predictions()
    patients = patient_service.get_all_patients()
    patient_dict = {p.id: p for p in patients}
    
    if not predictions:
        st.warning("No prediction data available yet. Make some predictions first!")
        return
    
    # Key Metrics Row
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", len(patients))
    with col2:
        st.metric("Total Predictions", len(predictions))
    with col3:
        high_risk = sum(1 for p in predictions if p.risk_level == "High")
        st.metric("High Risk Cases", high_risk, 
                 delta=f"{high_risk/len(predictions)*100:.1f}%", delta_color="inverse")
    with col4:
        avg_conf = sum((p.confidence or 0) for p in predictions) / len(predictions)
        st.metric("Avg Confidence", f"{avg_conf:.1f}%")
    
    st.markdown("---")
    
    # Chart 1: Risk Distribution Pie Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Risk Distribution")
        risk_counts = {'Low': 0, 'Medium': 0, 'High': 0}
        for p in predictions:
            if p.risk_level in risk_counts:
                risk_counts[p.risk_level] += 1
        
        fig = px.pie(
            values=list(risk_counts.values()),
            names=list(risk_counts.keys()),
            color=list(risk_counts.keys()),
            color_discrete_map={'Low': '#10B981', 'Medium': '#F59E0B', 'High': '#EF4444'},
            hole=0.4
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=350,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("#### Confidence Distribution")
        confidence_values = [p.confidence or 0 for p in predictions]
        
        fig = go.Figure(data=[go.Histogram(
            x=confidence_values,
            nbinsx=20,
            marker_color='#14B8A6'
        )])
        fig.update_layout(
            xaxis_title="Confidence %",
            yaxis_title="Count",
            margin=dict(l=20, r=20, t=40, b=20),
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Chart 2: Timeline Analysis
    st.markdown("#### Predictions Timeline")
    
    # Prepare timeline data
    timeline_data = []
    for p in predictions:
        if p.created_at:
            timeline_data.append({
                'Date': p.created_at.date(),
                'Risk Level': p.risk_level,
                'Count': 1
            })
    
    if timeline_data:
        df = pd.DataFrame(timeline_data)
        df_grouped = df.groupby(['Date', 'Risk Level']).sum().reset_index()
        
        fig = px.line(
            df_grouped,
            x='Date',
            y='Count',
            color='Risk Level',
            color_discrete_map={'Low': '#10B981', 'Medium': '#F59E0B', 'High': '#EF4444'},
            markers=True
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Chart 3: Age Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👥 Age Distribution")
        age_data = [p.age for p in patients if p.age]
        
        if age_data:
            fig = go.Figure(data=[go.Histogram(
                x=age_data,
                nbinsx=15,
                marker_color='#14B8A6'
            )])
            fig.update_layout(
                xaxis_title="Age",
                yaxis_title="Count",
                margin=dict(l=20, r=20, t=40, b=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("#### ⚖️ Gender Distribution")
        gender_counts = {'M': 0, 'F': 0}
        for p in patients:
            if p.gender in gender_counts:
                gender_counts[p.gender] += 1
        
        fig = px.bar(
            x=list(gender_counts.keys()),
            y=list(gender_counts.values()),
            labels={'x': 'Gender', 'y': 'Count'},
            color=list(gender_counts.keys()),
            color_discrete_map={'M': '#14B8A6', 'F': '#0D9488'}
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Chart 4: Risk by Age Group
    st.markdown("#### Risk Level by Age Group")
    
    age_risk_data = []
    for p in predictions:
        patient = patient_dict.get(p.patient_id)
        if patient and patient.age:
            age_group = f"{(patient.age // 10) * 10}-{(patient.age // 10) * 10 + 9}"
            age_risk_data.append({
                'Age Group': age_group,
                'Risk Level': p.risk_level,
                'Count': 1
            })
    
    if age_risk_data:
        df_age_risk = pd.DataFrame(age_risk_data)
        df_age_risk_grouped = df_age_risk.groupby(['Age Group', 'Risk Level']).sum().reset_index()
        
        fig = px.bar(
            df_age_risk_grouped,
            x='Age Group',
            y='Count',
            color='Risk Level',
            color_discrete_map={'Low': '#10B981', 'Medium': '#F59E0B', 'High': '#EF4444'},
            barmode='group'
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Summary Statistics Table
    st.markdown("---")
    st.markdown("### Detailed Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Risk Level Breakdown:**")
        for risk in ['Low', 'Medium', 'High']:
            count = sum(1 for p in predictions if p.risk_level == risk)
            pct = count / len(predictions) * 100 if predictions else 0
            st.write(f"• {risk}: {count} ({pct:.1f}%)")
    
    with col2:
        st.markdown("**Confidence Ranges:**")
        ranges = {'0-50%': 0, '50-75%': 0, '75-90%': 0, '90-100%': 0}
        for p in predictions:
            conf = p.confidence or 0
            if conf < 50:
                ranges['0-50%'] += 1
            elif conf < 75:
                ranges['50-75%'] += 1
            elif conf < 90:
                ranges['75-90%'] += 1
            else:
                ranges['90-100%'] += 1
        
        for range_name, count in ranges.items():
            pct = count / len(predictions) * 100 if predictions else 0
            st.write(f"• {range_name}: {count} ({pct:.1f}%)")
