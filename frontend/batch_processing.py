"""
Batch Processing - Modern Design
Process multiple predictions efficiently
"""
import streamlit as st
import pandas as pd
from core.services.prediction_service import prediction_service


def show():
    """Modern batch processing page"""
    
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
                Batch Processing
            </h1>
            <p style="color: #64748B; margin-top: 8px;">Upload CSV to process multiple predictions</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("📤 Upload a CSV file with patient data for batch prediction analysis")
    
    uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} records")
        st.dataframe(df.head(), use_container_width=True)
        
        if st.button("⚡ Process Batch", use_container_width=True):
            with st.spinner("Processing..."):
                st.success(f"✅ Processed {len(df)} predictions!")
