# CancerCare - Service Page
import streamlit as st

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .service-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid #00d9ff;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🏥 Our Services")
    
    services = [
        {
            "icon": "🤖",
            "title": "AI-Powered Risk Assessment",
            "description": "Advanced machine learning algorithms analyze patient data to provide accurate lung cancer risk predictions."
        },
        {
            "icon": "👥",
            "title": "Patient Management",
            "description": "Comprehensive patient record system with search, tracking, and history management."
        },
        {
            "icon": "📊",
            "title": "Data Analytics",
            "description": "Detailed statistical analysis and visualization of prediction results and patient data."
        },
        {
            "icon": "🔒",
            "title": "Secure Data Storage",
            "description": "Enterprise-grade PostgreSQL database with encrypted storage and JWT authentication."
        },
        {
            "icon": "📱",
            "title": "Real-Time Monitoring",
            "description": "Network performance tracking and system health monitoring."
        },
        {
            "icon": "📅",
            "title": "Appointment Scheduling",
            "description": "Priority-based appointment system with doctor and patient management."
        }
    ]
    
    for service in services:
        st.markdown(f"""
            <div class="service-card">
                <h2>{service['icon']} {service['title']}</h2>
                <p>{service['description']}</p>
            </div>
        """, unsafe_allow_html=True)
    
    if st.button("⬅️ Back to Home"):
        st.query_params.page = "home"
        st.rerun()
