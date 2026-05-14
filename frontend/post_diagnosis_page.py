"""
Post-Diagnosis Management - Modern Design
Clean tabs, medical image tracking, tumor markers, treatment plans
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.post_diagnosis_service import post_diagnosis_service
from core.services.image_service import image_service
from core.services.tumor_marker_service import tumor_marker_service
from core.services.patient_service import patient_service


def show():
    """Modern post-diagnosis management page"""
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;
        }
        
        .page-header {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(16px);
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 24px;
        }
        
        .info-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
            border: 1px solid #E2E8F0;
        }
        
        .metric-inline {
            display: inline-block;
            margin-right: 24px;
            padding: 8px 16px;
            background: #F0FDFA;
            border-radius: 8px;
            border-left: 3px solid #14B8A6;
        }
        
        .metric-label {
            font-size: 12px;
            color: #64748B;
            text-transform: uppercase;
            font-weight: 600;
        }
        
        .metric-value {
            font-size: 18px;
            color: #1F2937;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="page-header">
            <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                Post-Diagnosis Management
            </h1>
            <p style="color: #64748B; margin-top: 8px;">Track diagnosis, images, markers, and treatment</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Patient selector
    patients = patient_service.get_all_patients()
    
    if not patients:
        st.warning("⚠️ No patients found. Add a patient first.")
        return
    
    patient_options = {f"{p.name} (MRN: {p.mrn})": p for p in patients}
    selected_patient_name = st.selectbox("👤 Select Patient", list(patient_options.keys()))
    selected_patient = patient_options[selected_patient_name]
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Diagnosis", "🔬 Images", "📊 Tumor Markers", "💊 Treatment"])
    
    with tab1:
        st.markdown("### Diagnosis Information")
        
        diagnoses = post_diagnosis_service.get_patient_diagnoses(selected_patient.id)
        
        if diagnoses:
            for diag in diagnoses:
                st.markdown(f"""
                    <div class="info-card">
                        <div style="font-weight: 700; color: #1F2937; font-size: 18px; margin-bottom: 12px;">
                            {diag.diagnosis_type or 'General Diagnosis'}
                        </div>
                        <div style="color: #64748B; margin-bottom: 16px;">
                            Date: {diag.diagnosis_date.strftime('%B %d, %Y') if diag.diagnosis_date else 'N/A'} | 
                            Stage: {diag.cancer_stage or 'N/A'}
                        </div>
                        <div style="color: #475569;">
                            {diag.diagnosis_notes or 'No notes available'}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📝 No diagnosis records yet")
            
            with st.form("add_diagnosis"):
                st.subheader("Add Diagnosis")
                diagnosis_type = st.text_input("Type", placeholder="e.g., Lung Adenocarcinoma")
                cancer_stage = st.selectbox("Stage", ["I", "II", "III", "IV"])
                diagnosis_date = st.date_input("Date")
                notes = st.text_area("Notes")
                
                if st.form_submit_button("💾 Save Diagnosis"):
                    post_diagnosis_service.create_diagnosis(
                        patient_id=selected_patient.id,
                        diagnosis_type=diagnosis_type,
                        cancer_stage=cancer_stage,
                        diagnosis_date=diagnosis_date,
                        diagnosis_notes=notes
                    )
                    st.success("✅ Diagnosis saved!")
                    st.rerun()
    
    with tab2:
        st.markdown("### Medical Images")
        
        # Get patient diagnoses for image association
        diagnoses = post_diagnosis_service.get_patient_diagnoses(selected_patient.id)
        
        # Image upload
        with st.form("upload_image"):
            st.subheader("Upload Medical Image")
            
            if diagnoses:
                diagnosis_options = {f"{d.diagnosis_type} - {d.diagnosis_date.strftime('%m/%d/%Y') if d.diagnosis_date else 'N/A'}": d 
                                   for d in diagnoses}
                selected_diag_name = st.selectbox("Associated Diagnosis", list(diagnosis_options.keys()))
                selected_diagnosis = diagnosis_options[selected_diag_name]
                diagnosis_id = selected_diagnosis.id
            else:
                st.warning("⚠️ Create a diagnosis first")
                diagnosis_id = None
            
            uploaded_file = st.file_uploader("Choose Image", type=['png', 'jpg', 'jpeg', 'dcm'])
            image_type = st.selectbox("Image Type", ["CT Scan", "X-Ray", "MRI", "PET Scan"])
            
            if st.form_submit_button("📤 Upload & Analyze") and uploaded_file and diagnosis_id:
                with st.spinner("Analyzing image..."):
                    result = image_service.upload_image(
                        patient_id=selected_patient.id,
                        post_diagnosis_id=diagnosis_id,
                        image_file=uploaded_file,
                        image_type=image_type
                    )
                    st.success("✅ Image uploaded and analyzed!")
                    st.rerun()
        
        # Display images
        images = image_service.get_patient_images(selected_patient.id)
        
        if images:
            st.markdown(f"**{len(images)} images** on file")
            
            for img in images[:10]:
                with st.expander(f"{img.image_type} - {img.upload_date.strftime('%b %d, %Y')}"):
                    try:
                        st.image(img.file_path, width=400)
                    except:
                        st.info("Image file not found")
                    
                    if img.ai_analyzed:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Tumor Detected", "Yes" if img.tumor_detected else "No")
                            if img.tumor_count:
                                st.metric("Count", img.tumor_count)
                        with col2:
                            st.metric("Confidence", f"{img.confidence_score:.1f}%" if img.confidence_score else "N/A")
                            if img.largest_tumor_size:
                                st.metric("Size (mm)", f"{img.largest_tumor_size:.1f}")
                        
                        if img.aggression_level:
                            color = ["#10B981", "#F59E0B", "#EF4444"][min(img.aggression_level-1, 2) if img.aggression_level <= 3 else 2]
                            st.markdown(f"""
                                <div style="background: {color}22; padding: 12px; border-radius: 8px; border-left: 3px solid {color};">
                                    <div style="font-weight: 600; color: {color};">Aggression Level: {img.aggression_level}/5</div>
                                    <div style="color: #64748B; font-size: 14px;">{img.aggression_description or ''}</div>
                                </div>
                            """, unsafe_allow_html=True)
        else:
            st.info("📷 No images uploaded yet")
    
    with tab3:
        st.markdown("### Tumor Markers")
        
        diagnoses = post_diagnosis_service.get_patient_diagnoses(selected_patient.id)
        
        if not diagnoses:
            st.warning("⚠️ Create a diagnosis first")
        else:
            diagnosis_options = {f"{d.diagnosis_type} - {d.diagnosis_date.strftime('%m/%d/%Y') if d.diagnosis_date else 'N/A'}": d 
                               for d in diagnoses}
            selected_diag_name = st.selectbox("Select Diagnosis", list(diagnosis_options.keys()), key="marker_diag")
            selected_diagnosis = diagnosis_options[selected_diag_name]
            
            # Add marker
            with st.form("add_marker"):
                st.subheader("Add Tumor Marker")
                col1, col2, col3 = st.columns(3)
                with col1:
                    marker_name = st.text_input("Marker Name", placeholder="e.g., CEA")
                with col2:
                    marker_value = st.number_input("Value", min_value=0.0, step=0.1)
                with col3:
                    test_date = st.date_input("Test Date")
                
                if st.form_submit_button("💾 Add Marker"):
                    tumor_marker_service.add_tumor_marker(
                        post_diagnosis_id=selected_diagnosis.id,
                        marker_name=marker_name,
                        marker_value=marker_value,
                        test_date=test_date
                    )
                    st.success("✅ Marker added!")
                    st.rerun()
            
            # Display markers
            markers = tumor_marker_service.get_diagnosis_markers(selected_diagnosis.id)
            
            if markers:
                for marker in markers:
                    st.markdown(f"""
                        <div class="info-card">
                            <div style="font-weight: 700; color: #14B8A6; font-size: 16px;">
                                {marker.marker_name}: {marker.marker_value}
                            </div>
                            <div style="color: #64748B; font-size: 14px; margin-top: 4px;">
                                {marker.test_date.strftime('%B %d, %Y') if marker.test_date else 'N/A'}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📊 No tumor markers recorded yet")
    
    with tab4:
        st.markdown("### Treatment Plan")
        
        diagnoses = post_diagnosis_service.get_patient_diagnoses(selected_patient.id)
        
        if diagnoses:
            for diag in diagnoses:
                if diag.treatment_plan:
                    st.markdown(f"""
                        <div class="info-card">
                            <div style="font-weight: 700; color: #1F2937; font-size: 18px; margin-bottom: 12px;">
                                Treatment for {diag.diagnosis_type}
                            </div>
                            <div style="color: #475569; line-height: 1.6;">
                                {diag.treatment_plan}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(f"📋 No treatment plan for {diag.diagnosis_type}")
        else:
            st.info("📋 No diagnoses to show treatment for")
