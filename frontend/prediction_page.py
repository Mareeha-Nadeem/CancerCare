# frontend/prediction_page.py
import streamlit as st
import pandas as pd

# optional – we'll write this helper in ml_utils next
# from data_science.ml_utils import predict_from_inputs

def show():
    # ---------- GLOBAL STYLE ----------
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #5EC2FF;
        }
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        # .pred-card {
        #     background: #FFFFFF;
        #     border-radius: 24px;
        #     padding: 2rem 2.5rem;
        #     max-width: 1050px;
        #     margin: 3rem auto 4rem auto;
        #     box-shadow: 0 14px 35px rgba(0,0,0,0.15);
        # }
        .pred-title {
            font-size: 2.1rem;
            font-weight: 900;
            color: #0050A3;
            margin-bottom: 0.3rem;
        }
        .pred-subtitle {
            font-size: 0.98rem;
            color: #555;
            margin-bottom: 1.3rem;
        }
        div.stButton > button:first-child {
            background-color: #FF6B1A;
            color: white;
            font-weight: 700;
            border-radius: 999px;
            padding: 0.55rem 1.8rem;
            border: none;
            font-size: 0.9rem;
        }
        div.stButton > button:first-child:hover {
            background-color: #ff8745;
        }
        </style>
    """, unsafe_allow_html=True)

    # st.markdown('<div class="pred-card">', unsafe_allow_html=True)

    # ---------- HEADER ----------
    st.markdown('<div class="pred-title">Lung Cancer Risk Prediction</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pred-subtitle">'
        'Fill in the patient details below to estimate the risk of lung cancer. '
        'This tool is for academic use only and is not a medical diagnosis.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ---------- FORM ----------
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        gender = st.selectbox("Gender", ["Male", "Female"])
        smoking = st.selectbox("Smoking", ["Yes", "No"])
        yellow_fingers = st.selectbox("Yellow Fingers", ["Yes", "No"])
        anxiety = st.selectbox("Anxiety", ["Yes", "No"])
        peer_pressure = st.selectbox("Peer Pressure", ["Yes", "No"])
        chronic_disease = st.selectbox("Chronic Disease", ["Yes", "No"])

    with col2:
        fatigue = st.selectbox("Fatigue", ["Yes", "No"])
        allergy = st.selectbox("Allergy", ["Yes", "No"])
        wheezing = st.selectbox("Wheezing", ["Yes", "No"])
        alcohol = st.selectbox("Alcohol Consumption", ["Yes", "No"])
        coughing = st.selectbox("Persistent Coughing", ["Yes", "No"])
        shortness = st.selectbox("Shortness of Breath", ["Yes", "No"])
        chest_pain = st.selectbox("Chest Pain", ["Yes", "No"])

    st.markdown("---")

    btn_col1, btn_col2 = st.columns([1, 1])

    with btn_col1:
        predict_clicked = st.button("Predict Risk")

    with btn_col2:
        if st.button("⬅ Back to Home"):
            st.session_state["current_page"] = "🏠 Home"
            st.rerun()

    # ---------- PREDICTION ----------
    if predict_clicked:
        # map yes/no → 1/0 (match your training encoding)
        inputs = {
            "AGE": age,
            "GENDER": 1 if gender == "Male" else 0,  # adjust if you encoded differently
            "SMOKING": 1 if smoking == "Yes" else 0,
            "YELLOW_FINGERS": 1 if yellow_fingers == "Yes" else 0,
            "ANXIETY": 1 if anxiety == "Yes" else 0,
            "PEER_PRESSURE": 1 if peer_pressure == "Yes" else 0,
            "CHRONIC_DISEASE": 1 if chronic_disease == "Yes" else 0,
            "FATIGUE": 1 if fatigue == "Yes" else 0,
            "ALLERGY": 1 if allergy == "Yes" else 0,
            "WHEEZING": 1 if wheezing == "Yes" else 0,
            "ALCOHOL_CONSUMING": 1 if alcohol == "Yes" else 0,
            "COUGHING": 1 if coughing == "Yes" else 0,
            "SHORTNESS_OF_BREATH": 1 if shortness == "Yes" else 0,
            "CHEST_PAIN": 1 if chest_pain == "Yes" else 0,
        }

        try:
            label, proba = predict_from_inputs(inputs)

            if label == "High Risk":
                st.error(f"Result: **{label}** ({proba:.1%} probability)")
            else:
                st.success(f"Result: **{label}** ({proba:.1%} probability)")

            with st.expander("View model input"):
                st.write(pd.DataFrame([inputs]))

        except Exception as e:
            st.error("Prediction failed. Check that the model and feature names match your dataset.")
            st.exception(e)

    st.markdown('</div>', unsafe_allow_html=True)  # close card
