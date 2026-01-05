"""
Reports & Export - Advanced with Filters
"""
import streamlit as st
from core.services.prediction_service import prediction_service
from core.services.patient_service import patient_service
import pandas as pd
from datetime import datetime, timedelta


def show():
    """Advanced reports page with filters"""
    
    st.markdown("""
        <style>
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        .filter-section {
            background: white; border-radius: 12px; padding: 20px; margin: 16px 0;
            border: 1px solid #E2E8F0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="page-header">
            <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                Reports & Export
            </h1>
            <p style="color: #64748B; margin-top: 8px;">Generate filtered reports and export data</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Filters Section
    st.markdown("### 🔍 Filters")
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_filter = st.multiselect("Risk Level", ["Low", "Medium", "High"], default=["Low", "Medium", "High"])
        
    with col2:
        date_from = st.date_input("From Date", datetime.now() - timedelta(days=30))
        
    with col3:
        date_to = st.date_input("To Date", datetime.now())
    
    col1, col2 = st.columns(2)
    with col1:
        min_confidence = st.slider("Min Confidence %", 0, 100, 0)
    with col2:
        gender_filter = st.multiselect("Gender", ["M", "F"], default=["M", "F"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get and filter predictions
    all_predictions = prediction_service.get_all_predictions()
    all_patients = {p.id: p for p in patient_service.get_all_patients()}
    
    filtered_predictions = []
    for pred in all_predictions:
        # Apply filters
        if pred.risk_level not in risk_filter:
            continue
        if pred.created_at and (pred.created_at.date() < date_from or pred.created_at.date() > date_to):
            continue
        if (pred.confidence or 0) < min_confidence:
            continue
        
        patient = all_patients.get(pred.patient_id)
        if patient and patient.gender not in gender_filter:
            continue
            
        filtered_predictions.append(pred)
    
    st.success(f"📊 **{len(filtered_predictions)} predictions** match your filters")
    
    # Report Type Selection
    st.markdown("### 📈 Available Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Summary Report", use_container_width=True):
            if filtered_predictions:
                df = pd.DataFrame([{
                    'Patient ID': p.patient_id,
                    'Patient Name': all_patients.get(p.patient_id).name if all_patients.get(p.patient_id) else 'Unknown',
                    'Risk Level': p.risk_level,
                    'Confidence %': (p.confidence or 0),
                    'Date': p.created_at.strftime('%Y-%m-%d') if p.created_at else 'N/A'
                } for p in filtered_predictions])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No data matches filters")
    
    with col2:
        if st.button("📊 Risk Distribution", use_container_width=True):
            if filtered_predictions:
                risk_counts = {}
                for p in filtered_predictions:
                    risk_counts[p.risk_level] = risk_counts.get(p.risk_level, 0) + 1
                
                st.write("**Risk Distribution:**")
                for risk, count in risk_counts.items():
                    pct = count / len(filtered_predictions) * 100
                    st.metric(f"{risk} Risk", f"{count} ({pct:.1f}%)")
            else:
                st.warning("No data matches filters")
    
    with col3:
        if st.button("📅 Timeline Report", use_container_width=True):
            if filtered_predictions:
                df = pd.DataFrame([{
                    'Date': p.created_at.strftime('%Y-%m-%d') if p.created_at else 'N/A',
                    'Risk Level': p.risk_level,
                    'Count': 1
                } for p in filtered_predictions])
                timeline = df.groupby(['Date', 'Risk Level']).count().reset_index()
                st.dataframe(timeline, use_container_width=True)
            else:
                st.warning("No data matches filters")
    
    # Export Options
    st.markdown("### 💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬇️ Download CSV", use_container_width=True):
            if filtered_predictions:
                df = pd.DataFrame([{
                    'Patient_ID': p.patient_id,
                    'Patient_Name': all_patients.get(p.patient_id).name if all_patients.get(p.patient_id) else 'Unknown',
                    'MRN': all_patients.get(p.patient_id).mrn if all_patients.get(p.patient_id) else 'N/A',
                    'Age': all_patients.get(p.patient_id).age if all_patients.get(p.patient_id) else 'N/A',
                    'Gender': all_patients.get(p.patient_id).gender if all_patients.get(p.patient_id) else 'N/A',
                    'Risk_Level': p.risk_level,
                    'Confidence': (p.confidence or 0),
                    'Prediction_Date': p.created_at.strftime('%Y-%m-%d %H:%M:%S') if p.created_at else 'N/A'
                } for p in filtered_predictions])
                
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download Filtered Report",
                    csv,
                    f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No data to export")
    
    with col2:
        if st.button("📊 Export Statistics", use_container_width=True):
            if filtered_predictions:
                stats = {
                    'Total Predictions': len(filtered_predictions),
                    'High Risk': sum(1 for p in filtered_predictions if p.risk_level == 'High'),
                    'Medium Risk': sum(1 for p in filtered_predictions if p.risk_level == 'Medium'),
                    'Low Risk': sum(1 for p in filtered_predictions if p.risk_level == 'Low'),
                    'Avg Confidence': sum((p.confidence or 0) for p in filtered_predictions) / len(filtered_predictions),
                    'Date From': date_from.strftime('%Y-%m-%d'),
                    'Date To': date_to.strftime('%Y-%m-%d')
                }
                
                stats_df = pd.DataFrame([stats])
                csv = stats_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Statistics",
                    csv,
                    f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    use_container_width=True
                )
    
    with col3:
        st.info("💡 **Tip:** Adjust filters above to customize your report")
