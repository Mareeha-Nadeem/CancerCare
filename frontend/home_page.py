"""
CancerCare - Modern Dark-Themed Home Page
"""
import streamlit as st
from datetime import datetime

def show():
    # Apply dark theme CSS
    st.markdown("""
        <style>
        /* Global Styles - Black Theme */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0.9);
            backdrop-filter: blur(10px);
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
            border-right: 1px solid #00d9ff;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        p, span, div {
            color: #e0e0e0 !important;
        }
        
        /* Hero Section */
        .hero-container {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            border: 2px solid #00d9ff;
            box-shadow: 0 10px 40px rgba(0, 217, 255, 0.3);
            margin: 2rem 0;
            text-align: center;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            text-shadow: 0 0 30px rgba(0, 217, 255, 0.5);
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
            color: #b0b0b0;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        .hero-tagline {
            font-size: 1.1rem;
            color: #00d9ff;
            font-weight: 600;
            margin-top: 1rem;
        }
        
        /* Feature Cards */
        .feature-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid #00d9ff;
            margin: 1rem 0;
            transition: all 0.3s ease;
            box-shadow: 0 5px 20px rgba(0, 217, 255, 0.2);
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 217, 255, 0.4);
            border-color: #ff006e;
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .feature-title {
            font-size: 1.5rem;
            color: #00d9ff;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .feature-desc {
            color: #b0b0b0;
            line-height: 1.6;
        }
        
        /* Stats Section */
        .stat-box {
            background: linear-gradient(135deg, #ff006e 0%, #ffbe0b 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem;
            box-shadow: 0 10px 30px rgba(255, 0, 110, 0.3);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 900;
            color: #ffffff;
        }
        
        .stat-label {
            font-size: 1rem;
            color: #ffffff;
            opacity: 0.9;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            color: #ffffff;
            font-weight: 700;
            border: none;
            border-radius: 50px;
            padding: 0.8rem 2.5rem;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 5px 20px rgba(0, 217, 255, 0.4);
        }
        
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 30px rgba(255, 0, 110, 0.6);
        }
        
        /* Info Boxes */
        .info-box {
            background: rgba(0, 217, 255, 0.1);
            border-left: 4px solid #00d9ff;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .warning-box {
            background: rgba(255, 190, 11, 0.1);
            border-left: 4px solid #ffbe0b;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        /* Divider */
        .gradient-divider {
            height: 2px;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            margin: 2rem 0;
            border-radius: 2px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">🫁 CancerCare</h1>
            <p class="hero-subtitle">
                Advanced Lung Cancer Risk Prediction System<br>
                Powered by Machine Learning & Modern Technology
            </p>
            <p class="hero-tagline">
                ⚡ Real-time Analysis | 🔒 Secure | 🎯 Accurate
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("## 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔬 Start Prediction", use_container_width=True):
            st.query_params.page = "prediction"
            st.rerun()
    
    with col2:
        if st.button("👥 View Patients", use_container_width=True):
            st.query_params.page = "patients"
            st.rerun()
    
    with col3:
        if st.button("👨‍⚕️ Doctors Portal", use_container_width=True):
            st.query_params.page = "doctors"
            st.rerun()
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # About Section with Features
    st.markdown("## ✨ Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI-Powered Predictions</div>
                <div class="feature-desc">
                    Advanced machine learning model trained on comprehensive medical data 
                    to provide accurate lung cancer risk assessment.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Comprehensive Analytics</div>
                <div class="feature-desc">
                    Detailed risk analysis with confidence scores, probability distributions,
                    and personalized recommendations.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <div class="feature-title">Secure & Private</div>
                <div class="feature-desc">
                    Enterprise-grade security with encrypted data storage, JWT authentication,
                    and complete patient privacy protection.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Real-Time Processing</div>
                <div class="feature-desc">
                    Instant predictions with network monitoring, real-time updates,
                    and optimized performance using advanced DSA techniques.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("## 🛠️ Technology Integration")
    
    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
    
    with tech_col1:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-number">📚</div>
                <div class="stat-label">Data Structures</div>
            </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-number">🧬</div>
                <div class="stat-label">Data Science</div>
            </div>
        """, unsafe_allow_html=True)
    
    with tech_col3:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-number">🌐</div>
                <div class="stat-label">Networks</div>
            </div>
        """, unsafe_allow_html=True)
    
    with tech_col4:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-number">⚙️</div>
                <div class="stat-label">Engineering</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Information Section
    st.markdown("## ℹ️ Important Information")
    
    st.markdown("""
        <div class="info-box">
            <strong>🎓 Academic Project</strong><br>
            This system integrates concepts from Data Structures & Algorithms, 
            Data Science, Computer Networks, and Software Engineering.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Medical Disclaimer</strong><br>
            This tool is for educational and assessment purposes only. 
            Always consult qualified healthcare professionals for medical decisions.
        </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center; color: #b0b0b0; padding: 2rem;">
            <p>🏥 CancerCare System | Built with ❤️ using Modern Technologies</p>
            <p style="font-size: 0.9rem;">© {datetime.now().year} | All Rights Reserved</p>
        </div>
    """, unsafe_allow_html=True)
