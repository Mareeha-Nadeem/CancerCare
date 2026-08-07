"""
Batch Processing — runs real predictions for every row in an uploaded CSV
"""
import streamlit as st
import pandas as pd
from core.services.prediction_service import prediction_service
from core.services.patient_service import patient_service
from datetime import datetime

# Expected columns the CSV must contain (matches ML model feature names)
REQUIRED_COLUMNS = [
    'AGE', 'GENDER', 'AIR_POLLUTION', 'ALCOHOL_USE', 'DUST_ALLERGY',
    'OCCUPATIONAL_HAZARDS', 'GENETIC_RISK', 'CHRONIC_LUNG_DISEASE',
    'BALANCED_DIET', 'OBESITY', 'SMOKING', 'PASSIVE_SMOKER',
    'CHEST_PAIN', 'COUGHING_OF_BLOOD', 'FATIGUE', 'WEIGHT_LOSS',
    'SHORTNESS_OF_BREATH', 'WHEEZING', 'SWALLOWING_DIFFICULTY',
    'CLUBBING_OF_FINGER_NAILS', 'FREQUENT_COLD', 'DRY_COUGH', 'SNORING',
]

def show():
    st.markdown("""
        <style>
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255,255,255,0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="page-header">
            <h1 style="font-size:32px;font-weight:800;background:linear-gradient(135deg,#14B8A6,#0D9488);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;">
                Batch Processing
            </h1>
            <p style="color:#64748B;margin-top:8px;">
                Upload a CSV file to run AI predictions on multiple patients at once
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Template download hint
    with st.expander("📋 Required CSV columns"):
        st.write("Your CSV must contain these columns (case-insensitive):")
        st.code(", ".join(REQUIRED_COLUMNS))
        st.caption("GENDER: 1 = Male, 2 = Female. All other columns: scale 1–8.")

    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

    if not uploaded_file:
        return

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return

    # Normalise column names to uppercase
    df.columns = [c.strip().upper() for c in df.columns]

    # Check for required columns
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        st.error(f"Missing columns: {', '.join(missing_cols)}")
        return

    st.success(f"✅ Loaded **{len(df)} records**")
    st.dataframe(df.head(5), use_container_width=True)

    if not st.button("⚡ Run Batch Predictions", use_container_width=True):
        return

    results = []
    progress = st.progress(0)
    status_text = st.empty()

    for i, row in df.iterrows():
        status_text.text(f"Processing record {i + 1} / {len(df)} …")

        # Auto-create patient record
        patient_data = {
            "name": str(row.get("NAME", f"Batch_Patient_{i+1}")),
            "age":  int(row.get("AGE", 50)),
            "gender": "M" if str(row.get("GENDER", "1")) in ("1", "M", "m") else "F",
            "mrn":  str(row.get("MRN", f"BATCH{datetime.now().strftime('%Y%m%d')}{i+1:04d}")),
        }
        patient, _ = patient_service.create_patient(patient_data)
        if patient is None:
            # Patient may already exist — look up by MRN
            all_patients = patient_service.get_all_patients()
            patient = next((p for p in all_patients if p.mrn == patient_data["mrn"]), None)

        if patient is None:
            results.append({"Row": i + 1, "Risk": "Error", "Confidence": 0, "Note": "Could not create patient"})
            progress.progress((i + 1) / len(df))
            continue

        features = {col: float(row[col]) for col in REQUIRED_COLUMNS if col in row.index}
        prediction, err = prediction_service.generate_prediction(patient.id, features)

        if err or prediction is None:
            results.append({"Row": i + 1, "Patient": patient_data["name"], "Risk": "Error",
                            "Confidence %": 0, "Note": err or "Prediction failed"})
        else:
            results.append({
                "Row":          i + 1,
                "Patient":      patient_data["name"],
                "MRN":          patient_data["mrn"],
                "Risk Level":   prediction.risk_level,
                "Confidence %": round(prediction.confidence, 1),
            })

        progress.progress((i + 1) / len(df))

    status_text.text("Done!")

    results_df = pd.DataFrame(results)
    st.markdown("### Results")
    st.dataframe(results_df, use_container_width=True)

    # Colour-coded summary
    if "Risk Level" in results_df.columns:
        counts = results_df["Risk Level"].value_counts()
        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 High Risk",   counts.get("High",   0))
        col2.metric("🟡 Medium Risk", counts.get("Medium", 0))
        col3.metric("🟢 Low Risk",    counts.get("Low",    0))

    # Download
    csv_out = results_df.to_csv(index=False)
    st.download_button("⬇️ Download Results CSV", csv_out,
                       file_name="batch_results.csv", mime="text/csv")
