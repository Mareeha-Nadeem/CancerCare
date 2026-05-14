"""
Advanced Search - Multiple Filters
"""
import streamlit as st
from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service
from datetime import datetime, timedelta


def show():
    """Advanced search with filters"""
    
    st.markdown("""
        <style>
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        .result-card {
            background: white; border-radius: 12px; padding: 16px; margin: 12px 0;
            border-left: 4px solid #14B8A6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="page-header">
            <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                Advanced Search
            </h1>
            <p style="color: #64748B; margin-top: 8px;">Search patients and predictions with advanced filters</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Search Type
    search_type = st.radio("Search Type", ["Patients", "Predictions", "Both"], horizontal=True)
    
    # Advanced Filters
    st.markdown("### 🔍 Search Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        text_search = st.text_input("Name / MRN", placeholder="Search...")
        age_range = st.slider("Age Range", 0, 120, (0, 120))
    
    with col2:
        gender_filter = st.multiselect("Gender", ["M", "F"], default=["M", "F"])
        risk_filter = st.multiselect("Risk Level", ["Low", "Medium", "High"], default=["Low", "Medium", "High"])
    
    with col3:
        date_from = st.date_input("From Date", datetime.now() - timedelta(days=90))
        date_to = st.date_input("To Date", datetime.now())
    
    confidence_range = st.slider("Confidence Range %", 0, 100, (0, 100))
    
    if st.button("🔍 Search", use_container_width=True):
        # Get all data
        patients = patient_service.get_all_patients()
        predictions = prediction_service.get_all_predictions()
        
        # Create patient lookup
        patient_dict = {p.id: p for p in patients}
        
        # Filter patients
        filtered_patients = []
        if search_type in ["Patients", "Both"]:
            for patient in patients:
                # Text search
                if text_search and text_search.lower() not in patient.name.lower() and \
                   (not patient.mrn or text_search.lower() not in patient.mrn.lower()):
                    continue
                
                # Age filter
                if patient.age < age_range[0] or patient.age > age_range[1]:
                    continue
                
                # Gender filter
                if patient.gender not in gender_filter:
                    continue
                
                filtered_patients.append(patient)
        
        # Filter predictions
        filtered_predictions = []
        if search_type in ["Predictions", "Both"]:
            for pred in predictions:
                patient = patient_dict.get(pred.patient_id)
                
                # Risk filter
                if pred.risk_level not in risk_filter:
                    continue
                
                # Confidence filter
                conf = (pred.confidence or 0)
                if conf < confidence_range[0] or conf > confidence_range[1]:
                    continue
                
                # Date filter
                if pred.created_at:
                    if pred.created_at.date() < date_from or pred.created_at.date() > date_to:
                        continue
                
                # Patient filters
                if patient:
                    if text_search and text_search.lower() not in patient.name.lower():
                        continue
                    if patient.age < age_range[0] or patient.age > age_range[1]:
                        continue
                    if patient.gender not in gender_filter:
                        continue
                
                filtered_predictions.append((pred, patient))
        
        # Display Results
        st.markdown("---")
        st.markdown(f"### 📊 Search Results")
        
        if search_type in ["Patients", "Both"] and filtered_patients:
            st.success(f"👥 **{len(filtered_patients)} patients** found")
            
            for patient in filtered_patients:
                st.markdown(f"""
                    <div class="result-card">
                        <div style="font-weight: 700; color: #1F2937; font-size: 18px;">{patient.name}</div>
                        <div style="color: #64748B; margin-top: 4px;">
                            MRN: {patient.mrn or 'N/A'} | Age: {patient.age} | Gender: {patient.gender}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        if search_type in ["Predictions", "Both"] and filtered_predictions:
            st.success(f"📋 **{len(filtered_predictions)} predictions** found")
            
            for pred, patient in filtered_predictions:
                risk_color = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}.get(pred.risk_level, "#64748B")
                patient_name = patient.name if patient else f"Patient #{pred.patient_id}"
                
                st.markdown(f"""
                    <div class="result-card" style="border-left-color: {risk_color};">
                        <div style="font-weight: 700; color: #1F2937;">{patient_name}</div>
                        <div style="color: {risk_color}; font-weight: 600; margin-top: 4px;">
                            {pred.risk_level} Risk - {(pred.confidence or 0):.1f}%
                        </div>
                        <div style="color: #64748B; font-size: 14px; margin-top: 4px;">
                            {pred.created_at.strftime('%B %d, %Y') if pred.created_at else 'N/A'}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        if (search_type in ["Patients", "Both"] and not filtered_patients and
            search_type in ["Predictions", "Both"] and not filtered_predictions) or \
           (search_type == "Patients" and not filtered_patients) or \
           (search_type == "Predictions" and not filtered_predictions):
            st.info("🔍 No results found. Try adjusting your filters.")
    
    # Quick Stats
    st.markdown("---")
    st.markdown("### 📈 Quick Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_patients = len(patient_service.get_all_patients())
    total_predictions = len(prediction_service.get_all_predictions())
    
    with col1:
        st.metric("Total Patients", total_patients)
    with col2:
        st.metric("Total Predictions", total_predictions)
    with col3:
        high_risk = sum(1 for p in prediction_service.get_all_predictions() if p.risk_level == "High")
        st.metric("High Risk", high_risk)
    with col4:
        avg_conf = sum((p.confidence or 0) for p in prediction_service.get_all_predictions()) / max(total_predictions, 1)
        st.metric("Avg Confidence", f"{avg_conf:.1f}%")
