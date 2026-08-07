"""
Prediction Page - Modern Clean Design
Efficient form layout with professional results visualization
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.prediction_service import prediction_service
from core.services.patient_service import patient_service
import plotly.graph_objects as go
from datetime import datetime


def show():
    """Display modern prediction page"""
    
    # Modern CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;
        }
        
        /* Page Header */
        .pred-header {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(16px);
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 32px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            text-align: center;
        }
        
       .pred-title {
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Form Section */
        .form-section {
            background: var(--bg-surface-elevated);
            border-radius: 12px;
            padding: 24px;
            margin: 16px 0;
            border: 1px solid #E2E8F0;
        }
        
        .section-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #14B8A6;
        }
        
        /* Risk Result Card */
        .risk-result {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 40px;
            margin: 32px 0;
            text-align: center;
        }
        
        .risk-high {
            border: 3px solid #EF4444;
            box-shadow: 0 12px 32px rgba(239, 68, 68, 0.3);
        }
        
        .risk-medium {
            border: 3px solid #F59E0B;
            box-shadow: 0 12px 32px rgba(245, 158, 11, 0.3);
        }
        
        .risk-low {
            border: 3px solid #10B981;
            box-shadow: 0 12px 32px rgba(16, 185, 129, 0.3);
        }
        
        .risk-value {
            font-size: 72px;
            font-weight: 900;
            margin: 16px 0;
        }
        
        .risk-label {
            font-size: 24px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="pred-header">
            <h1 class="pred-title">AI Risk Prediction</h1>
            <p style="color: var(--text-muted); font-size: 16px; margin-top: 8px;">
                Enter patient data for lung cancer risk assessment
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None
    
    with st.form("prediction_form"):
        # Patient Info
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Patient Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("Patient Name", placeholder="Full Name")
            age = st.number_input("Age", min_value=1, max_value=120, value=50)
        with col2:
            mrn = st.text_input("MRN", placeholder="Medical Record Number (optional)")
            gender = st.selectbox("Gender", ["M", "F"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Lifestyle Factors
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🌍 Lifestyle & Environmental</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            smoking = st.slider("Smoking", 1, 8, 4)
            passive_smoker = st.slider("Passive Smoking", 1, 8, 3)
            air_pollution = st.slider("Air Pollution", 1, 8, 4)
        with col2:
            alcohol_use = st.slider("Alcohol Use", 1, 8, 3)
            dust_allergy = st.slider("Dust Allergy", 1, 8, 3)
            occupational_hazards = st.slider("Occupational Hazards", 1, 8, 3)
        with col3:
            balanced_diet = st.slider("Diet Quality", 1, 8, 5)
            obesity = st.slider("Obesity", 1, 8, 3)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Symptoms & Clinical
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Clinical Symptoms</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            genetic_risk = st.slider("Genetic Risk", 1, 8, 3)
            coughing_of_blood = st.slider("Coughing Blood", 1, 8, 2)
            weight_loss = st.slider("Weight Loss", 1, 8, 2)
            snoring = st.slider("Snoring", 1, 8, 3)
        with col2:
            chronic_lung_disease = st.slider("Chronic Lung Disease", 1, 8, 3)
            wheezing = st.slider("Wheezing", 1, 8, 3)
            shortness_of_breath = st.slider("Shortness of Breath", 1, 8, 3)
        with col3:
            chest_pain = st.slider("Chest Pain", 1, 8, 3)
            swallowing_difficulty = st.slider("Swallowing Difficulty", 1, 8, 2)
            frequent_cold = st.slider("Frequent Cold", 1, 8, 3)
        with col4:
            fatigue = st.slider("Fatigue", 1, 8, 3)
            clubbing_of_finger_nails = st.slider("Finger Clubbing", 1, 8, 2)
            dry_cough = st.slider("Dry Cough", 1, 8, 3)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit Button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("🔮 Predict Risk", use_container_width=True)
    
    # Process prediction
    if submitted:
        with st.spinner("Analyzing patient data..."):
            # Create or get patient
            patient_data = {
                'name': patient_name if patient_name else f"Patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'age': age,
                'gender': gender,
                'mrn': mrn if mrn else f"MRN{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            patient, error = patient_service.create_patient(patient_data)
            
            if error:
                # Patient might already exist, try to get by MRN
                patients = patient_service.get_all_patients()
                patient = next((p for p in patients if p.mrn == patient_data['mrn']), None)
                if not patient:
                    st.error(f"Error creating patient: {error}")
                    st.stop()
            
            # Prediction features
            # All 23 features matching the trained ML model schema exactly
            features = {
                'AGE':                    age,
                'GENDER':                 1 if gender == "M" else 2,
                'AIR_POLLUTION':          air_pollution,
                'ALCOHOL_USE':            alcohol_use,
                'DUST_ALLERGY':           dust_allergy,
                'OCCUPATIONAL_HAZARDS':   occupational_hazards,
                'GENETIC_RISK':           genetic_risk,
                'CHRONIC_LUNG_DISEASE':   chronic_lung_disease,
                'BALANCED_DIET':          balanced_diet,
                'OBESITY':                obesity,
                'SMOKING':                smoking,
                'PASSIVE_SMOKER':         passive_smoker,
                'CHEST_PAIN':             chest_pain,
                'COUGHING_OF_BLOOD':      coughing_of_blood,
                'FATIGUE':                fatigue,
                'WEIGHT_LOSS':            weight_loss,
                'SHORTNESS_OF_BREATH':    shortness_of_breath,
                'WHEEZING':               wheezing,
                'SWALLOWING_DIFFICULTY':  swallowing_difficulty,
                'CLUBBING_OF_FINGER_NAILS': clubbing_of_finger_nails,
                'FREQUENT_COLD':          frequent_cold,
                'DRY_COUGH':              dry_cough,
                'SNORING':                snoring,
            }
            
            # Get prediction
            prediction, error = prediction_service.generate_prediction(patient.id, features)
            
            if error:
                st.error(f"Prediction error: {error}")
                st.stop()
            
            # Convert to result format for display
            result = {
                'risk_level': prediction.risk_level,
                'risk_probability': prediction.confidence,
                'confidence': prediction.confidence
            }
            
            st.session_state.prediction_result = result
    
    # Display Results
    if st.session_state.prediction_result:
        result = st.session_state.prediction_result
        
        # Risk card with color coding
        risk_class = f"risk-{result['risk_level'].lower()}"
        risk_color = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}.get(result['risk_level'], "#64748B")
        
        st.markdown(f"""
            <div class="risk-result {risk_class}">
                <div class="risk-label" style="color: {risk_color};">{result['risk_level']} RISK</div>
                <div class="risk-value" style="color: {risk_color};">{result['risk_probability']:.1f}%</div>
                <p style="color: var(--text-muted); font-size: 16px; margin-top: 16px;">
                    Confidence Score: {result['confidence']:.1f}%
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Risk gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result['risk_probability'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Score", 'font': {'size': 20, 'family': 'Inter'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': risk_color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#E2E8F0",
                'steps': [
                    {'range': [0, 33], 'color': '#D1FAE5'},
                    {'range': [33, 66], 'color': '#FEF3C7'},
                    {'range': [66, 100], 'color': '#FEE2E2'}
                ],
                'threshold': {
                    'line': {'color': risk_color, 'width': 4},
                    'thickness': 0.75,
                    'value': result['risk_probability']
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Recommendations
        st.markdown("""
            <div class="form-section">
                <div class="section-title">Recommendations</div>
            </div>
        """, unsafe_allow_html=True)
        
        if result['risk_level'] == "High":
            st.error("**Immediate medical consultation recommended.** Schedule comprehensive screening and diagnostic tests.")
        elif result['risk_level'] == "Medium":
            st.warning("**Follow-up recommended.** Schedule routine screening and monitor symptoms closely.")
        else:
            st.success("**Low risk detected.** Maintain healthy lifestyle and regular check-ups.")
