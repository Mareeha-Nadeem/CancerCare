"""
Landing Page - World-Class Design
Premium medical UI with glassmorphism
"""
import streamlit as st


def show():
    """Display ultra-modern landing page"""
    
    # Ultra-premium CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        /* Glassmorphic Background */
        .stApp {
            background: linear-gradient(135deg, #F0FDFA 0%, #E0F2FE 50%, #F0F9FF 100%) !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Hero Section */
        .hero-container {
            padding: 80px 20px;
            text-align: center;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .hero-title {
            font-size: 72px;
            font-weight: 800;
            background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 24px;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }
        
        .hero-subtitle {
            font-size: 24px;
            color: #475569;
            font-weight: 500;
            margin-bottom: 48px;
            line-height: 1.5;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Glassmorphic CTAs */
        .cta-container {
            display: flex;
            gap: 16px;
            justify-content: center;
            margin-bottom: 100px;
        }
        
        .cta-primary {
            background: #14B8A6 !important;
            color: white !important;
            padding: 16px 40px !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            border: none !important;
            box-shadow: 0 8px 24px rgba(20, 184, 166, 0.35) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        .cta-primary:hover {
            background: #0D9488 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 32px rgba(20, 184, 166, 0.45) !important;
        }
        
        .cta-secondary {
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(10px) !important;
            color: #14B8A6 !important;
            padding: 16px 40px !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            border: 2px solid rgba(20, 184, 166, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .cta-secondary:hover {
            background: white !important;
            border-color: #14B8A6 !important;
            transform: translateY(-2px) !important;
        }
        
        /* Glassmorphic Feature Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 20px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
        }
        
        .glass-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.25);
            border-color: rgba(20, 184, 166, 0.3);
        }
        
        .feature-icon {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            margin-bottom: 24px;
            box-shadow: 0 4px 16px rgba(20, 184, 166, 0.3);
        }
        
        .feature-title {
            font-size: 24px;
            font-weight: 700;
            color: #1F2937;
            margin-bottom: 12px;
        }
        
        .feature-desc {
            font-size: 16px;
            color: #64748B;
            line-height: 1.6;
        }
        
        /* Stats Section */
        .stats-container {
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(16px);
            border-radius: 24px;
            padding: 60px 40px;
            margin: 80px 0;
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 48px;
            font-weight: 800;
            background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        
        .stat-label {
            font-size: 16px;
            color: #64748B;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">AI-Powered Cancer Care Platform</h1>
            <p class="hero-subtitle">
                Advanced machine learning meets compassionate healthcare. 
                Predict risks, analyze images, and manage patient care with unprecedented precision.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_login, col_signup = st.columns(2)
        with col_login:
            if st.button("Get Started", key="get_started", use_container_width=True):
                st.session_state.page = "auth"
                st.session_state.auth_mode = "signup"
                st.rerun()
        with col_signup:
            if st.button("Sign In", key="sign_in", use_container_width=True):
                st.session_state.page = "auth"
                st.session_state.auth_mode = "login"
                st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Features Grid
    st.markdown("<h2 style='text-align: center; font-size: 42px; font-weight: 700; margin: 80px 0 60px 0; color: #1F2937;'>Comprehensive Cancer Care Suite</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">🧬</div>
                <div class="feature-title">ML Risk Prediction</div>
                <div class="feature-desc">
                    Advanced machine learning algorithms analyze patient data to predict lung cancer risk with high accuracy.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">🔬</div>
                <div class="feature-title">Image Analysis</div>
                <div class="feature-desc">
                    AI-powered medical image analysis detects tumors, calculates size, position, mass, and aggression levels.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Post-Diagnosis Tracking</div>
                <div class="feature-desc">
                    Comprehensive patient management with treatment tracking, tumor markers, and progress visualization.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">👥</div>
                <div class="feature-title">Patient Management</div>
                <div class="feature-desc">
                    Centralized patient records, appointment scheduling, and medical history management in one place.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Batch Processing</div>
                <div class="feature-desc">
                    Process multiple patient predictions simultaneously with our efficient batch processing system.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="glass-card">
                <div class="feature-icon">📈</div>
                <div class="feature-title">Advanced Analytics</div>
                <div class="feature-desc">
                    Real-time dashboard with insights, trends, and comprehensive reporting capabilities.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
        <div class="stats-container">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div class="stat-item">
                    <div class="stat-number">95%</div>
                    <div class="stat-label">Prediction Accuracy</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">10K+</div>
                    <div class="stat-label">Patients Analyzed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">50K+</div>
                    <div class="stat-label">Images Processed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">AI Monitoring</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 60px 20px; color: #94A3B8;">
            <p style="font-size: 16px; margin-bottom: 12px;">
                CancerCare © 2026 | Powered by Advanced AI & Machine Learning
            </p>
            <p style="font-size: 14px;">
                Professional healthcare technology for better patient outcomes
            </p>
        </div>
    """, unsafe_allow_html=True)
