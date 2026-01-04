"""
Landing Page
Professional healthcare-themed landing page with feature showcase
"""
import streamlit as st


def show():
    """Display the landing page"""
    
    # Custom CSS for healthcare theme
    st.markdown("""
        <style>
        /* Main page styling */
        .stApp {
            background: linear-gradient(135deg, #1e7e8c 0%, #2c9db0 100%);
        }
        
        /* Header styling */
        .landing-header {
            text-align: center;
            padding: 60px 20px 40px 20px;
            color: white;
        }
        
        .landing-header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .landing-header p {
            font-size: 1.3rem;
            opacity: 0.95;
            margin-bottom: 30px;
        }
        
        /* Feature card styling */
        .feature-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 35px 25px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transition: transform 0.3s ease;
            margin: 20px 0;
            height: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.2);
        }
        
        .feature-icon {
            font-size: 3.5rem;
            margin-bottom: 20px;
            color: #1e7e8c;
        }
        
        .feature-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1e7e8c;
            margin-bottom: 15px;
        }
        
        .feature-description {
            font-size: 1rem;
            color: #555;
            line-height: 1.6;
        }
        
        /* Button styling */
        .auth-buttons {
            text-align: center;
            margin: 40px 0;
        }
        
        .stButton > button {
            background: white;
            color: #1e7e8c;
            border: 2px solid white;
            padding: 15px 45px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 30px;
            margin: 0 10px;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: #1e7e8c;
            color: white;
            transform: scale(1.05);
        }
        
        /* Info section */
        .info-section {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 40px 0;
        }
        
        .info-section h3 {
            font-size: 1.8rem;
            margin-bottom: 15px;
        }
        
        /* Footer */
        .landing-footer {
            text-align: center;
            padding: 30px;
            color: white;
            opacity: 0.8;
            margin-top: 60px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="landing-header">
            <h1>CancerCare</h1>
            <p>Intelligent Cancer Diagnosis & Patient Management System</p>
            <p style="font-size: 1.1rem; opacity: 0.9;">
                AI-Powered Risk Assessment | Medical Image Analysis | Comprehensive Care Tracking
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Auth buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-buttons">', unsafe_allow_html=True)
        col_login, col_signup = st.columns(2)
        
        with col_login:
            if st.button("Login", use_container_width=True):
                st.session_state.page = "auth"
                st.session_state.auth_mode = "login"
                st.rerun()
        
        with col_signup:
            if st.button("Sign Up", use_container_width=True):
                st.session_state.page = "auth"
                st.session_state.auth_mode = "signup"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
        <div class="info-section">
            <h3>Platform Features</h3>
            <p style="font-size: 1.1rem;">
                Comprehensive cancer care management powered by artificial intelligence
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon"></div>
                <div class="feature-title">AI Risk Prediction</div>
                <div class="feature-description">
                    Advanced machine learning models predict lung cancer risk with 91% accuracy. 
                    Analyze 23 risk factors for comprehensive assessment.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon"></div>
                <div class="feature-title">Medical Image Analysis</div>
                <div class="feature-description">
                    Automated AI analysis of CT scans, MRI, and X-rays. 
                    Instant abnormality detection with confidence scoring.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon"></div>
                <div class="feature-title">Treatment Monitoring</div>
                <div class="feature-description">
                    Track tumor markers, visualize trends, and monitor treatment 
                    effectiveness with comprehensive analytics.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Second row of features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon"></div>
                <div class="feature-title">Patient Management</div>
                <div class="feature-description">
                    Complete patient profiles with medical history, predictions, 
                    and comprehensive timeline tracking.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon"></div>
                <div class="feature-title">Appointment System</div>
                <div class="feature-description">
                    Streamlined scheduling, doctor management, and patient-physician 
                    coordination for efficient care.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon"></div>
                <div class="feature-title">Analytics & Reports</div>
                <div class="feature-description">
                    Comprehensive reporting, batch processing, and population 
                    health analytics for data-driven decisions.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Additional Info
    st.markdown("""
        <div class="info-section">
            <h3>Powered by Advanced Technology</h3>
            <p style="font-size: 1rem; line-height: 1.8;">
                <strong>Machine Learning:</strong> Gradient Boosting + ResNet50 Deep Learning<br>
                <strong>Database:</strong> PostgreSQL with 9 integrated tables<br>
                <strong>Features:</strong> 15+ interactive modules for complete care management<br>
                <strong>Performance:</strong> <1 second predictions | 85%+ image analysis accuracy
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="landing-footer">
            <p style="font-size: 0.9rem;">
                CancerCare - Intelligent Laboratory Management System<br>
                © 2025 | Powered by AI & Machine Learning
            </p>
        </div>
    """, unsafe_allow_html=True)
