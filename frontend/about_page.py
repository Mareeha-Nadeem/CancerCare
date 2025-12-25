# CancerCare - About Page
import streamlit as st

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("ℹ️ About CancerCare")
    
    st.markdown("""
    ## 🎓 Academic Project
    
    CancerCare is a comprehensive lung cancer risk prediction system that integrates concepts from multiple computer science disciplines:
    
    ### 📚 Course Integration
    
    **1. Data Structures & Algorithms**
    - Priority Queue for appointment scheduling
    - Binary Search Tree for patient indexing
    - Hash Tables for quick data lookups
    - Efficient search and sort algorithms
    
    **2. Introduction to Data Science**
    - Machine Learning model for risk prediction
    - Feature engineering and preprocessing
    - Model evaluation and validation
    - Statistical analysis and visualization
    
    **3. Computer Networks**
    - HTTP request/response logging
    - Network performance monitoring
    - Session management with JWT tokens
    - Real-time statistics tracking
    - TCP/IP protocol demonstration
    
    **4. Software Engineering**
    - Full-stack development
    - Database design with PostgreSQL
    - RESTful service architecture
    - Code organization and modularity
    - Documentation and version control
    
    ### 🛠️ Technology Stack
    
    - **Frontend:** Streamlit with custom CSS
    - **Backend:** Python with SQLAlchemy ORM
    - **Database:** PostgreSQL
    - **ML Framework:** Scikit-learn
    - **Authentication:** JWT tokens with bcrypt
    - **Visualization:** Plotly
    
    ### ⚠️ Disclaimer
    
    This application is designed for educational and research purposes only. 
    It should not be used as a substitute for professional medical advice, 
    diagnosis, or treatment. Always consult qualified healthcare professionals 
    for medical decisions.
    """)
    
    if st.button("⬅️ Back to Home"):
        st.query_params.page = "home"
        st.rerun()
