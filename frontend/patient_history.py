"""
Patient History - Modern Design  
View patient prediction history
"""
import streamlit as st
from core.services.prediction_service import prediction_service
from core.services.patient_service import patient_service


def show():
    """Modern patient history page"""
    
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
                Patient History
            </h1>
            <p style="color: var(--text-muted); margin-top: 8px;">View prediction history by patient</p>
        </div>
    """, unsafe_allow_html=True)
    
    patients = patient_service.get_all_patients()
    
    if patients:
        patient_options = {f"{p.name} (MRN: {p.mrn})": p for p in patients}
        selected_name = st.selectbox("Select Patient", list(patient_options.keys()))
        selected_patient = patient_options[selected_name]
        
        predictions = prediction_service.get_patient_predictions(selected_patient.id)
        
        if predictions:
            st.success(f"**{len(predictions)} predictions** found")
            for pred in predictions:
                risk_color = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}.get(pred.risk_level, "#64748B")
                confidence = getattr(pred, 'confidence', 0) or 0
                st.markdown(f"""
                    <div style="background: var(--bg-surface-elevated); padding: 16px; border-radius: 12px; margin: 12px 0; 
                         border-left: 4px solid {risk_color};">
                        <div style="font-weight: 700; color: {risk_color};">{pred.risk_level} Risk - {confidence:.1f}%</div>
                        <div style="color: var(--text-muted); font-size: 14px; margin-top: 4px;">
                            {pred.created_at.strftime('%B %d, %Y') if pred.created_at else 'N/A'}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No predictions yet for this patient")
    else:
        st.warning("No patients found")
