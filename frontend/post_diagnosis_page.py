"""
Post-Diagnosis Management Page
Complete 5-tab interface for diagnosis tracking, medical images, tumor markers, and treatment
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.post_diagnosis_service import post_diagnosis_service
from core.services.image_service import image_service
from core.services.tumor_marker_service import tumor_marker_service
from core.services.patient_service import patient_service

def show():
    """Main post-diagnosis page"""
    
    # Dark theme CSS
    st.markdown("""
        <style>
        .diagnosis-header {
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
        .metric-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #00d9ff;
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="diagnosis-header">
            <h1 class="page-title"> Post-Diagnosis Management</h1>
            <p style="color: #b0b0b0;">Comprehensive cancer care tracking and monitoring</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Patient selector
    st.subheader(" Select Patient")
    patients = patient_service.get_all_patients()
    
    if not patients:
        st.warning(" No patients found. Please add a patient first.")
        return
    
    patient_options = {f"{p.name} (MRN: {p.mrn})": p for p in patients}
    selected_patient_name = st.selectbox(
        "Patient",
        options=list(patient_options.keys()),
        label_visibility="collapsed"
    )
    
    selected_patient = patient_options[selected_patient_name]
    
    st.markdown("---")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        " Diagnosis Info",
        " Medical Images",
        " Tumor Markers",
        " Treatment Plan",
        " Progress Timeline"
    ])
    
    with tab1:
        show_diagnosis_tab(selected_patient)
    
    with tab2:
        show_images_tab(selected_patient)
    
    with tab3:
        show_markers_tab(selected_patient)
    
    with tab4:
        show_treatment_tab(selected_patient)
    
    with tab5:
        show_timeline_tab(selected_patient)


def show_diagnosis_tab(patient):
    """Tab 1: Diagnosis Information"""
    st.subheader(" Diagnosis Information")
    
    # Get existing diagnoses
    diagnoses = post_diagnosis_service.get_patient_diagnosis(patient.id)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Add/Update Diagnosis")
        
        with st.form("diagnosis_form"):
            diagnosis_date = st.date_input("Diagnosis Date", datetime.now())
            
            cancer_type = st.selectbox(
                "Cancer Type",
                ["Lung Cancer", "Breast Cancer", "Colon Cancer", "Prostate Cancer", 
                 "Liver Cancer", "Pancreatic Cancer", "Other"]
            )
            
            stage = st.selectbox(
                "Stage",
                ["Stage I", "Stage II", "Stage III", "Stage IV", "Unknown"]
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                tumor_size = st.number_input("Tumor Size (mm)", min_value=0.0, value=0.0, step=0.1)
            with col_b:
                lymph_nodes = st.number_input("Lymph Nodes Affected", min_value=0, value=0, step=1)
            
            metastasis = st.selectbox(
                "Metastasis Status",
                ["None", "Regional", "Distant"]
            )
            
            treatment_plan = st.text_area("Treatment Plan", height=100)
            notes = st.text_area("Doctor's Notes", height=100)
            
            submitted = st.form_submit_button(" Save Diagnosis", use_container_width=True)
            
            if submitted:
                diagnosis_data = {
                    'diagnosis_date': datetime.combine(diagnosis_date, datetime.min.time()),
                    'cancer_type': cancer_type,
                    'stage': stage,
                    'tumor_size_mm': tumor_size,
                    'lymph_nodes_affected': lymph_nodes,
                    'metastasis_status': metastasis,
                    'treatment_plan': treatment_plan,
                    'notes': notes
                }
                
                diagnosis, error = post_diagnosis_service.create_diagnosis(
                    patient_id=patient.id,
                    data=diagnosis_data
                )
                
                if error:
                    st.error(f" Error: {error}")
                else:
                    st.success(" Diagnosis saved successfully!")
                    st.rerun()
    
    with col2:
        st.markdown("### Recent Diagnoses")
        if diagnoses:
            for diag in diagnoses[:3]:
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{diag.cancer_type}</strong><br/>
                    Stage: {diag.stage}<br/>
                    Date: {diag.diagnosis_date.strftime('%Y-%m-%d')}<br/>
                    Tumor: {diag.tumor_size_mm} mm
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ No diagnoses recorded yet")


def show_images_tab(patient):
    """Tab 2: Medical Images"""
    st.subheader(" Medical Images")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload New Image")
        
        image_type = st.selectbox(
            "Image Type",
            ["MRI", "CT Scan", "X-Ray", "PET Scan", "Ultrasound"]
        )
        
        uploaded_file = st.file_uploader(
            "Choose medical image",
            type=['jpg', 'jpeg', 'png'],
            help="Supported formats: JPEG, PNG (max 50MB)"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Preview", use_column_width=True)
            
            if st.button(" Upload & Analyze", use_container_width=True):
                with st.spinner("Uploading and analyzing..."):
                    # Get latest diagnosis
                    diagnoses = post_diagnosis_service.get_patient_diagnosis(patient.id)
                    diag_id = diagnoses[0].id if diagnoses else None
                    
                    # Upload with AI analysis
                    image, error = image_service.upload_image(
                        patient_id=patient.id,
                        image_file=uploaded_file,
                        image_type=image_type,
                        post_diagnosis_id=diag_id,
                        filename=uploaded_file.name,
                        auto_analyze=True
                    )
                    
                    if error:
                        st.error(f" {error}")
                    else:
                        st.success(" Image uploaded and analyzed!")
                        st.rerun()
    
    with col2:
        st.markdown("### Image Gallery")
        
        images = image_service.get_patient_images(patient.id)
        
        if images:
            for img in images[:5]:
                with st.expander(f"{img.image_type} - {img.upload_date.strftime('%Y-%m-%d')}"):
                    st.markdown(f"**File:** {Path(img.file_path).name}")
                    st.markdown(f"**Size:** {img.image_width}x{img.image_height} px")
                    
                    if img.ai_analyzed:
                        st.markdown("** AI Analysis:**")
                        result = " Abnormal" if img.tumor_detected else "🟢 Normal"
                        st.markdown(f"- Result: {result}")
                        st.markdown(f"- Confidence: {img.confidence_score:.1%}")
                        if img.tumor_count:
                            st.markdown(f"- Tumors: {img.tumor_count}")
                            st.markdown(f"- Largest: {img.largest_tumor_size:.1f} mm")
                    
                    # Display image
                    try:
                        st.image(img.file_path, use_column_width=True)
                    except:
                        st.info("Image preview not available")
        else:
            st.info("ℹ No images uploaded yet")


def show_markers_tab(patient):
    """Tab 3: Tumor Markers"""
    st.subheader(" Tumor Markers")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Add Marker Result")
        
        with st.form("marker_form"):
            marker_name = st.selectbox(
                "Marker",
                ["CEA", "CA 19-9", "CA 125", "PSA", "AFP", "CA 15-3", "CA 27-29"]
            )
            
            value = st.number_input("Value", min_value=0.0, step=0.1)
            test_date = st.date_input("Test Date", datetime.now())
            labname = st.text_input("Laboratory")
            
            submit = st.form_submit_button(" Record Marker", use_container_width=True)
            
            if submit:
                # Get latest diagnosis
                diagnoses = post_diagnosis_service.get_patient_diagnosis(patient.id)
                diag_id = diagnoses[0].id if diagnoses else None
                
                marker_data = {
                    'marker_name': marker_name,
                    'value': value,
                    'test_date': datetime.combine(test_date, datetime.min.time()),
                    'lab_name': lab_name
                }
                
                marker, error = tumor_marker_service.record_marker(
                    patient_id=patient.id,
                    marker_data=marker_data,
                    post_diagnosis_id=diag_id
                )
                
                if error:
                    st.error(f" {error}")
                else:
                    st.success(" Marker recorded!")
                    st.rerun()
    
    with col2:
        st.markdown("### Marker Trends")
        
        markers = tumor_marker_service.get_patient_markers(patient.id)
        
        if markers:
            # Group by marker name
            marker_data = {}
            for m in markers:
                if m.marker_name not in marker_data:
                    marker_data[m.marker_name] = []
                marker_data[m.marker_name].append({
                    'date': m.test_date,
                    'value': m.value,
                    'abnormal': m.is_abnormal
                })
            
            # Create trend chart
            selected_marker = st.selectbox(
                "Select marker to view trend",
                list(marker_data.keys())
            )
            
            if selected_marker:
                data = sorted(marker_data[selected_marker], key=lambda x: x['date'])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[d['date'] for d in data],
                    y=[d['value'] for d in data],
                    mode='lines+markers',
                    name=selected_marker,
                    line=dict(color='#00d9ff', width=3),
                    marker=dict(
                        size=10,
                        color=['red' if d['abnormal'] else 'green' for d in data]
                    )
                ))
                
                # Get reference range
                ranges = tumor_marker_service.get_reference_ranges()
                ref = ranges.get(selected_marker, {})
                if ref:
                    fig.add_hline(
                        y=ref['max'],
                        line_dash="dash",
                        line_color="red",
                        annotation_text=f"Max Normal: {ref['max']}"
                    )
                
                fig.update_layout(
                    title=f"{selected_marker} Trend Over Time",
                    xaxis_title="Date",
                    yaxis_title=f"Value ({ref.get('unit', 'U/mL')})",
                    template="plotly_dark",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Show recent results
            st.markdown("### Recent Results")
            for m in markers[:5]:
                status = "" if m.is_abnormal else "🟢"
                st.markdown(f"{status} **{m.marker_name}**: {m.value} {m.unit} ({m.test_date.strftime('%Y-%m-%d')})")
        else:
            st.info("ℹ No marker results recorded yet")



def show_treatment_tab(patient):
    """Tab 4: Treatment Plan"""
    st.subheader(" Treatment Plan")
    
    diagnoses = post_diagnosis_service.get_patient_diagnosis(patient.id)
    
    if diagnoses:
        st.markdown("### Current Treatment Plans")
        for diag in diagnoses:
            with st.expander(f"{diag.cancer_type} - {diag.stage}"):
                if diag.treatment_plan:
                    st.markdown(f"**Plan:** {diag.treatment_plan}")
                else:
                    st.info("No treatment plan recorded")
                
                if diag.notes:
                    st.markdown(f"**Notes:** {diag.notes}")
    else:
        st.info("ℹ No diagnoses found. Add diagnosis in Tab 1.")


def show_timeline_tab(patient):
    """Tab 5: Progress Timeline"""
    st.subheader(" Progress Timeline")
    
    # Collect all events
    events = []
    
    # Diagnoses
    diagnoses = post_diagnosis_service.get_patient_diagnosis(patient.id)
    for diag in diagnoses:
        events.append({
            'date': diag.diagnosis_date,
            'type': 'Diagnosis',
            'description': f"{diag.cancer_type} - {diag.stage}",
            'icon': ''
        })
    
    # Images
    images = image_service.get_patient_images(patient.id)
    for img in images:
        result = "Abnormal detected" if img.tumor_detected else "Normal"
        events.append({
            'date': img.upload_date,
            'type': 'Imaging',
            'description': f"{img.image_type} - {result}",
            'icon': ''
        })
    
    # Markers
    markers = tumor_marker_service.get_patient_markers(patient.id)
    for m in markers[:10]:  # Limit to recent
        status = "Abnormal" if m.is_abnormal else "Normal"
        events.append({
            'date': m.test_date,
            'type': 'Lab Test',
            'description': f"{m.marker_name}: {m.value} {m.unit} ({status})",
            'icon': ''
        })
    
    # Sort by date
    events.sort(key=lambda x: x['date'], reverse=True)
    
    if events:
        st.markdown("### Complete Medical Timeline")
        for event in events:
            st.markdown(f"""
            <div class="metric-card">
                {event['icon']} <strong>{event['type']}</strong><br/>
                {event['description']}<br/>
                <small style="color: #888;">{event['date'].strftime('%Y-%m-%d %H:%M')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ No events recorded yet")


if __name__ == "__main__":
    show()
