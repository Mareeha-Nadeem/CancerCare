"""
CancerCare - Modern Dark-Themed Prediction Page
Integrated with ML Model and Database
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.prediction_service import prediction_service
from core.services.patient_service import patient_service
from core.network_logger import network_logger
import plotly.graph_objects as go
import json
from datetime import datetime

def show():
    # Apply dark theme CSS
    st.markdown("""
        <style>
        /* Black Theme for Prediction Page */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .prediction-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #00d9ff;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.3);
        }
        
        .prediction-title {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .prediction-subtitle {
            color: #b0b0b0;
            font-size: 1.1rem;
        }
        
        /* Input Sections */
        .input-section {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #00d9ff;
            margin: 1rem 0;
        }
        
        .section-title {
            color: #00d9ff;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            border-bottom: 2px solid #00d9ff;
            padding-bottom: 0.5rem;
        }
        
        /* Result Card */
        .result-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            box-shadow: 0 15px 40px rgba(0, 217, 255, 0.3);
        }
        
        .result-high {
            border: 3px solid #ff006e;
            box-shadow: 0 15px 40px rgba(255, 0, 110, 0.4);
        }
        
        .result-medium {
            border: 3px solid #ffbe0b;
            box-shadow: 0 15px 40px rgba(255, 190, 11, 0.4);
        }
        
        .result-low {
            border: 3px solid #00ff88;
            box-shadow: 0 15px 40px rgba(0, 255, 136, 0.4);
        }
        
        .risk-label {
            font-size: 2rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .risk-high {
            color: #ff006e;
            text-shadow: 0 0 20px rgba(255, 0, 110, 0.5);
        }
        
        .risk-medium {
            color: #ffbe0b;
            text-shadow: 0 0 20px rgba(255, 190, 11, 0.5);
        }
        
        .risk-low {
            color: #00ff88;
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        }
        
        .confidence-text {
            text-align: center;
            font-size: 1.2rem;
            color: #e0e0e0;
            margin-top: 0.5rem;
        }
        
        /* Form Styling */
        .stSlider > div {
            background: rgba(0, 217, 255, 0.1);
            border-radius: 10px;
            padding: 0.5rem;
        }
        
        .stSelectbox > div {
            background: rgba(0, 217, 255, 0.1);
        }
        
        .stNumberInput > div {
            background: rgba(0, 217, 255, 0.1);
        }
        
        /* Gradient Divider */
        .gradient-divider {
            height: 2px;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            margin: 2rem 0;
            border-radius: 2px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="prediction-header">
            <h1 class="prediction-title">🔬 Lung Cancer Risk Prediction</h1>
            <p class="prediction-subtitle">
                Enter patient information below for AI-powered risk assessment
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None
    
    # Patient Information Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Patient Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        patient_name = st.text_input("Patient Name", placeholder="Enter patient full name", help="Patient's full name")
        age = st.number_input("Age", min_value=1, max_value=120, value=50, help="Patient's age in years")
    
    with col2:
        mrn = st.text_input("MRN (Medical Record Number)", placeholder="e.g., MRN001", help="Medical Record Number (optional - will be auto-generated if empty)")
        gender = st.selectbox("Gender", ["M", "F"], help="Patient's gender")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk Factors Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚬 Lifestyle & Environmental Risk Factors</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        smoking = st.slider("Smoking Level", 1, 8, 4, help="1 = Never, 8 = Heavy smoker")
        passive_smoker = st.slider("Passive Smoking Exposure", 1, 8, 3)
        air_pollution = st.slider("Air Pollution Exposure", 1, 8, 4)
    
    with col2:
        alcohol_use = st.slider("Alcohol Consumption", 1, 8, 3)
        dust_allergy = st.slider("Dust Allergy", 1, 8, 3)
        occupational_hazards = st.slider("Occupational Hazards", 1, 8, 3)
    
    with col3:
        balanced_diet = st.slider("Balanced Diet Quality", 1, 8, 5, help="1 = Poor, 8 = Excellent")
        obesity = st.slider("Obesity Level", 1, 8, 3)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Medical History Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏥 Medical History</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        genetic_risk = st.slider("Genetic Risk", 1, 8, 3)
        chronic_lung_disease = st.slider("Chronic Lung Disease", 1, 8, 3)
    
    with col2:
        chest_pain = st.slider("Chest Pain", 1, 8, 3)
        fatigue = st.slider("Fatigue Level", 1, 8, 3)
    
    with col3:
        weight_loss = st.slider("Weight Loss", 1, 8, 2)
        shortness_of_breath = st.slider("Shortness of Breath", 1, 8, 3)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Symptoms Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🩺 Symptoms</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        coughing_of_blood = st.slider("Coughing Blood", 1, 8, 2)
        wheezing = st.slider("Wheezing", 1, 8, 3)
    
    with col2:
        swallowing_difficulty = st.slider("Swallowing Difficulty", 1, 8, 2)
        clubbing_of_finger_nails = st.slider("Finger Clubbing", 1, 8, 2)
    
    with col3:
        frequent_cold = st.slider("Frequent Cold", 1, 8, 3)
        dry_cough = st.slider("Dry Cough", 1, 8, 3)
    
    with col4:
        snoring = st.slider("Snoring", 1, 8, 3)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Prediction Button
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        predict_button = st.button("🔮 Predict Risk Level", use_container_width=True, type="primary")
    
    # Make Prediction
    if predict_button:
        with st.spinner("🤖 Analyzing patient data..."):
            # Log network request
            request_id = network_logger.log_request(
                method="POST",
                endpoint="/predict",
                client_ip="127.0.0.1",
                user_agent="Streamlit"
            )
            
            start_time = datetime.now()
            
            # Prepare features
            features = {
                'age': age,
                'gender': gender,
                'smoking': smoking,
                'passive_smoker': passive_smoker,
                'air_pollution': air_pollution,
                'alcohol_use': alcohol_use,
                'dust_allergy': dust_allergy,
                'occupational_hazards': occupational_hazards,
                'genetic_risk': genetic_risk,
                'chronic_lung_disease': chronic_lung_disease,
                'balanced_diet': balanced_diet,
                'obesity': obesity,
                'chest_pain': chest_pain,
                'coughing_of_blood': coughing_of_blood,
                'fatigue': fatigue,
                'weight_loss': weight_loss,
                'shortness_of_breath': shortness_of_breath,
                'wheezing': wheezing,
                'swallowing_difficulty': swallowing_difficulty,
                'clubbing_of_finger_nails': clubbing_of_finger_nails,
                'frequent_cold': frequent_cold,
                'dry_cough': dry_cough,
                'snoring': snoring,
            }
            
            # Get or create patient
            patient = None
            
            # Validate patient name
            if not patient_name or patient_name.strip() == "":
                st.error("❌ Please enter a patient name")
                return
            
            # Generate MRN if not provided
            if not mrn or mrn.strip() == "":
                mrn = f"MRN{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Check if patient exists
            patient = patient_service.get_patient_by_mrn(mrn)
            
            if not patient:
                # Create new patient
                patient_data = {
                    'mrn': mrn,
                    'name': patient_name.strip(),
                    'age': age,
                    'gender': gender,
                    'contact': ""
                }
                patient, error = patient_service.create_patient(patient_data)
                if error:
                    st.error(f"Error creating patient: {error}")
                    return
                else:
                    st.success(f"✅ New patient created: {patient_name} (MRN: {mrn})")
            else:
                # Update existing patient info if needed
                st.info(f"ℹ️ Using existing patient: {patient.name} (MRN: {patient.mrn})")
            
            # Make prediction
            if patient:
                prediction, error = prediction_service.generate_prediction(patient.id, features)
                if error:
                    st.error(f"Prediction error: {error}")
                else:
                    # Parse probabilities
                    probabilities = json.loads(prediction.probabilities)
                    st.session_state.prediction_result = {
                        'risk_level': prediction.risk_level,
                        'confidence': prediction.confidence,
                        'probabilities': probabilities,
                        'patient_name': patient.name,
                        'patient_mrn': patient.mrn
                    }
                    
                    # Send email notification if patient has email
                    if patient.email:
                        try:
                            from core.email_service import email_service
                            
                            # Determine recommendations based on risk
                            if prediction.risk_level == "High":
                                recommendations = "URGENT: Schedule immediate consultation with an oncologist. Undergo comprehensive diagnostic testing including CT scan and biopsy."
                            elif prediction.risk_level == "Medium":
                                recommendations = "Schedule appointment with a pulmonologist. Monitor symptoms closely and consider follow-up screening in 3-6 months."
                            else:
                                recommendations = "Maintain current healthy lifestyle. Continue with regular health check-ups and avoid smoking."
                            
                            email_service.send_prediction_report(
                                patient_email=patient.email,
                                patient_name=patient.name,
                                risk_level=prediction.risk_level,
                                confidence=prediction.confidence,
                                recommendations=recommendations
                            )
                            st.success(f"📧 Prediction report sent to {patient.email}")
                        except Exception as e:
                            st.warning(f"Prediction saved but email notification failed: {e}")
            else:
                # Fallback: Make prediction without saving
                from core.services.ml_service import ml_service
                result = ml_service.predict(features)
                result['patient_name'] = patient_name
                result['patient_mrn'] = mrn if mrn else "N/A"
                st.session_state.prediction_result = result
            
            # Log response
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            network_logger.log_response(
                request_id=request_id,
                status_code=200,
                response_time_ms=response_time
            )
    
    # Display Results
    if st.session_state.prediction_result:
        result = st.session_state.prediction_result
        risk = result['risk_level']
        confidence = result['confidence']
        probs = result['probabilities']
        
        # Display patient info
        if 'patient_name' in result:
            st.info(f"👤 **Patient:** {result['patient_name']} | **MRN:** {result.get('patient_mrn', 'N/A')}")
        
        # Determine card style
        card_class = f"result-card result-{risk.lower()}"
        risk_class = f"risk-{risk.lower()}"
        
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        st.markdown(f'<div class="risk-label {risk_class}">⚠️ {risk.upper()} RISK</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="confidence-text">Confidence: {confidence:.1%}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Probability Distribution Chart
        st.subheader("📊 Risk Probability Distribution")
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(probs.keys()),
                y=list(probs.values()),
                marker=dict(
                    color=['#00ff88', '#ffbe0b', '#ff006e'],
                    line=dict(color='#00d9ff', width=2)
                ),
                text=[f'{v:.1%}' for v in probs.values()],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0', size=14),
            xaxis=dict(
                title="Risk Level",
                gridcolor='rgba(0, 217, 255, 0.2)',
                color='#e0e0e0'
            ),
            yaxis=dict(
                title="Probability",
                gridcolor='rgba(0, 217, 255, 0.2)',
                color='#e0e0e0'
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Recommendations")
        
        if risk == "High":
            st.error("""
                **Immediate Action Required:**
                - Schedule urgent consultation with an oncologist
                - Undergo comprehensive diagnostic testing
                - Consider CT scan and biopsy
                - Discuss treatment options immediately
            """)
        elif risk == "Medium":
            st.warning("""
                **Recommended Actions:**
                - Schedule appointment with a pulmonologist
                - Monitor symptoms closely
                - Consider follow-up screening in 3-6 months
                - Adopt healthy lifestyle changes
            """)
        else:
            st.success("""
                **Preventive Measures:**
                - Maintain current healthy lifestyle
                - Regular health check-ups
                - Avoid smoking and secondhand smoke
                - Stay physically active
            """)
        
        # Option to start new prediction
        if st.button("🔄 New Prediction"):
            st.session_state.prediction_result = None
            st.rerun()
    
    # Back to home
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home"):
        st.query_params.page = "home"
        st.rerun()
