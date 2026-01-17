"""
Batch Sample Processing for Lab Technicians
Process multiple patient samples at once
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service
from core.services.ml_service import ml_service
from core.notification_service import notification_service, notify_prediction_complete
import io

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .batch-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #00d9ff;
            margin-bottom: 2rem;
        }
        
        .batch-title {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00d9ff 0%, #ffbe0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="batch-header">
            <h1 class="batch-title"> Batch Sample Processing</h1>
            <p style="color: #b0b0b0;">Process multiple patient samples efficiently</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([" Upload Batch", " Quick Batch Entry", " Batch Results"])
    
    with tab1:
        st.subheader("Upload CSV File")
        
        st.info("""
        **CSV Format Requirements:**
        - Column: `mrn` (Medical Record Number)
        - Column: `age`
        - Column: `gender` (M/F)
        - Columns: All 23 risk factors (smoking, passive_smoker, air_pollution, etc.)
        """)
        
        # Download template
        if st.button(" Download CSV Template"):
            template_data = {
                'mrn': ['MRN001', 'MRN002'],
                'age': [65, 55],
                'gender': ['M', 'F'],
                'smoking': [7, 4],
                'passive_smoker': [3, 2],
                'air_pollution': [5, 4],
                'alcohol_use': [3, 2],
                'dust_allergy': [3, 3],
                'occupational_hazards': [4, 2],
                'genetic_risk': [6, 3],
                'chronic_lung_disease': [4, 2],
                'balanced_diet': [4, 6],
                'obesity': [5, 3],
                'chest_pain': [5, 2],
                'coughing_of_blood': [3, 1],
                'fatigue': [5, 3],
                'weight_loss': [4, 2],
                'shortness_of_breath': [5, 3],
                'wheezing': [4, 2],
                'swallowing_difficulty': [2, 1],
                'clubbing_of_finger_nails': [3, 1],
                'frequent_cold': [4, 3],
                'dry_cough': [5, 3],
                'snoring': [3, 2]
            }
            
            df_template = pd.DataFrame(template_data)
            csv = df_template.to_csv(index=False)
            
            st.download_button(
                label=" Download Template",
                data=csv,
                file_name="batch_template.csv",
                mime="text/csv"
            )
        
        # File upload
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
        
        if uploaded_file:
            try:
                # df = pd.DataFrame(uploaded_file)
                df = pd.read_csv(uploaded_file)
                
                st.success(f" File loaded: {len(df)} samples found")
                st.dataframe(df.head(), use_container_width=True)
                
                if st.button(" Process Batch", type="primary"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results = []
                    
                    for idx, row in df.iterrows():
                        status_text.text(f"Processing sample {idx+1}/{len(df)}...")
                        progress_bar.progress((idx + 1) / len(df))
                        
                        # Get or create patient
                        patient = patient_service.get_patient_by_mrn(row['mrn'])
                        
                        if not patient:
                            patient_data = {
                                'mrn': row['mrn'],
                                'name': f"Patient {row['mrn']}",
                                'age': int(row['age']),
                                'gender': row['gender'],
                                'contact': ""
                            }
                            patient, error = patient_service.create_patient(patient_data)
                        
                        # Prepare features
                        features = {col: row[col] for col in df.columns if col not in ['mrn', 'age', 'gender']}
                        features['age'] = int(row['age'])
                        features['gender'] = row['gender']
                        
                        # Make prediction
                        prediction, error = prediction_service.generate_prediction(
                            patient.id,
                            features
                        )
                        
                        if not error:
                            results.append({
                                'MRN': row['mrn'],
                                'Risk': prediction.risk_level,
                                'Confidence': f"{prediction.confidence:.1%}",
                                'Status': ' Success'
                            })
                            
                            # Notify for high risk
                            if prediction.risk_level == "High":
                                notify_prediction_complete(
                                    patient.name,
                                    prediction.risk_level,
                                    "all"
                                )
                        else:
                            results.append({
                                'MRN': row['mrn'],
                                'Risk': 'N/A',
                                'Confidence': 'N/A',
                                'Status': f' Error: {error}'
                            })
                    
                    st.success(" Batch processing complete!")
                    
                    # Show results
                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Download results
                    csv_results = results_df.to_csv(index=False)
                    st.download_button(
                        " Download Results",
                        csv_results,
                        f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
            
            except Exception as e:
                st.error(f"Error processing file: {e}")
    
    with tab2:
        st.subheader("Quick Batch Entry (Manual)")
        
        num_samples = st.number_input("Number of samples to process", min_value=1, max_value=20, value=3)
        
        st.write("Enter data for each sample:")
        
        batch_data = []
        
        for i in range(num_samples):
            with st.expander(f"Sample {i+1}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    mrn = st.text_input("MRN", key=f"mrn_{i}")
                    age = st.number_input("Age", 1, 120, 50, key=f"age_{i}")
                
                with col2:
                    gender = st.selectbox("Gender", ["M", "F"], key=f"gender_{i}")
                    smoking = st.slider("Smoking", 1, 8, 4, key=f"smoking_{i}")
                
                with col3:
                    genetic_risk = st.slider("Genetic Risk", 1, 8, 3, key=f"genetic_{i}")
                    chest_pain = st.slider("Chest Pain", 1, 8, 3, key=f"chest_{i}")
                
                if mrn:
                    batch_data.append({
                        'mrn': mrn,
                        'age': age,
                        'gender': gender,
                        'smoking': smoking,
                        'genetic_risk': genetic_risk,
                        'chest_pain': chest_pain,
                        # Add defaults for other features
                        'passive_smoker': 3,
                        'air_pollution': 4,
                        'alcohol_use': 3,
                        'dust_allergy': 3,
                        'occupational_hazards': 3,
                        'chronic_lung_disease': 3,
                        'balanced_diet': 5,
                        'obesity': 3,
                        'coughing_of_blood': 2,
                        'fatigue': 3,
                        'weight_loss': 2,
                        'shortness_of_breath': 3,
                        'wheezing': 3,
                        'swallowing_difficulty': 2,
                        'clubbing_of_finger_nails': 2,
                        'frequent_cold': 3,
                        'dry_cough': 3,
                        'snoring': 3
                    })
        
        if st.button(" Process All Samples", type="primary") and batch_data:
            st.write(f"Processing {len(batch_data)} samples...")
            
            for data in batch_data:
                patient = patient_service.get_patient_by_mrn(data['mrn'])
                
                if not patient:
                    patient_data = {
                        'mrn': data['mrn'],
                        'name': f"Patient {data['mrn']}",
                        'age': data['age'],
                        'gender': data['gender'],
                        'contact': ""
                    }
                    patient, _ = patient_service.create_patient(patient_data)
                
                prediction, _ = prediction_service.generate_prediction(
                    patient.id,
                    data
                )
            
            st.success(" All samples processed!")
            st.balloons()
    
    with tab3:
        st.subheader("Recent Batch Results")
        
        # Show recent predictions grouped by time
        predictions = prediction_service.get_all_predictions(limit=50)
        
        if predictions:
            st.write(f"**Total Recent Tests:** {len(predictions)}")
            
            # Group by date
            from collections import defaultdict
            by_date = defaultdict(list)
            
            for pred in predictions:
                date_key = pred.created_at.strftime('%Y-%m-%d')
                by_date[date_key].append(pred)
            
            for date, preds in sorted(by_date.items(), reverse=True):
                with st.expander(f" {date} ({len(preds)} tests)"):
                    for pred in preds:
                        patient = patient_service.get_patient_by_id(pred.patient_id)
                        if patient:
                            risk_emoji = {'High': '', 'Medium': '🟡', 'Low': '🟢'}
                            st.write(f"{risk_emoji[pred.risk_level]} {patient.name} (MRN: {patient.mrn}) - {pred.risk_level} ({pred.confidence:.1%})")
        else:
            st.info("No batch results yet")
    
    # Back button
    st.markdown("---")
    if st.button(" Back to Lab Dashboard"):
        st.query_params.page = "lab_dashboard"
        st.rerun()
