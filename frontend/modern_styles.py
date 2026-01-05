"""
Premium Glassmorphic Theme
Single Color Palette - Medical Teal
Ultra-Modern with Transparency Effects
Inspired by: Apple, Stripe, Linear
"""

MODERN_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* ========== SINGLE COLOR SYSTEM - MEDICAL TEAL ========== */
    :root {
        /* Primary - Medical Teal (ONLY accent color) */
        --accent: #14B8A6;
        --accent-hover: #0D9488;
        --accent-light: #CCFBF1;
        --accent-ultra-light: #F0FDFA;
        
        /* Neutral Palette */
        --white: #FFFFFF;
        --gray-50: #FAFAFA;
        --gray-100: #F4F4F5;
        --gray-200: #E4E4E7;
        --gray-300: #D4D4D8;
        --gray-400: #A1A1AA;
        --gray-600: #52525B;
        --gray-900: #18181B;
        
        /* Glassmorphism */
        --glass-bg: rgba(255, 255, 255, 0.7);
        --glass-border: rgba(255, 255, 255, 0.18);
        
        /* Shadows */
        --shadow-glass: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* ========== GLOBAL GLASSMORPHIC BASE ========== */
    .stApp {
        background: linear-gradient(135deg, #FAFAFA 0%, #F0FDFA 100%) !important;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        letter-spacing: -0.01em;
    }
    
    /* Remove default margins */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* ========== GLASSMORPHIC CONTAINERS ========== */
    .element-container,
    [data-testid="column"],
    .stTabs [data-baseweb="tab-panel"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-radius: 16px !important;
        border: 1px solid var(--glass-border) !important;
        box-shadow: var(--shadow-glass) !important;
    }
    
    /* ========== TYPOGRAPHY ========== */
    h1, h2, h3 {
        color: var(--gray-900) !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }
    
    h4, h5, h6 {
        color: var(--gray-900) !important;
        font-weight: 600 !important;
    }
    
    p, span, div, label {
        color: var(--gray-600) !important;
        line-height: 1.6 !important;
    }
    
    /* ========== BUTTONS - TEAL ACCENT ========== */
    .stButton > button {
        background: var(--accent) !important;
        color: var(--white) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px 0 rgba(20, 184, 166, 0.35) !important;
    }
    
    .stButton > button:hover {
        background: var(--accent-hover) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px 0 rgba(20, 184, 166, 0.45) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* ========== GLASSMORPHIC INPUTS ========== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(10px) !important;
        border: 1.5px solid var(--gray-300) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        color: var(--gray-900) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus-within,
    .stDateInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px var(--accent-ultra-light) !important;
        outline: none !important;
    }
    
    /* ========== GLASSMORPHIC SIDEBAR ========== */
    [data-testid="stSidebar"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: var(--gray-900) !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        background: transparent !important;
        padding: 12px 16px !important;
        border-radius: 10px !important;
        margin: 3px 0 !important;
        color: var(--gray-600) !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        border: 1px solid transparent !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: var(--accent-ultra-light) !important;
        color: var(--gray-900) !important;
        border-color: var(--accent-light) !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label[data-checked="true"] {
        background: var(--accent-light) !important;
        color: var(--accent-hover) !important;
        font-weight: 600 !important;
        border-color: var(--accent) !important;
    }
    
    /* ========== GLASSMORPHIC METRICS ========== */
    [data-testid="stMetric"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px) !important;
        padding: 24px !important;
        border-radius: 16px !important;
        border: 1px solid var(--glass-border) !important;
        box-shadow: var(--shadow-glass) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: var(--gray-600) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: var(--accent) !important;
    }
    
    /* ========== GLASSMORPHIC TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        padding: 6px !important;
        gap: 4px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--gray-600) !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--accent-ultra-light) !important;
        color: var(--gray-900) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--white) !important;
        color: var(--accent) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    /* ========== GLASSMORPHIC EXPANDERS ========== */
    .streamlit-expanderHeader {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-weight: 600 !important;
        color: var(--gray-900) !important;
        transition: all 0.2s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--accent-light) !important;
        background: var(--white) !important;
    }
    
    /* ========== STATUS MESSAGES - TEAL ACCENT ========== */
    .stSuccess {
        background: linear-gradient(135deg, var(--accent-ultra-light) 0%, var(--accent-light) 100%) !important;
        border-left: 4px solid var(--accent) !important;
        color: var(--accent-hover) !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stError {
        background: rgba(254, 226, 226, 0.8) !important;
        border-left: 4px solid #EF4444 !important;
        color: #991B1B !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stWarning {
        background: rgba(254, 243, 199, 0.8) !important;
        border-left: 4px solid #F59E0B !important;
        color: #92400E !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stInfo {
        background: var(--accent-ultra-light) !important;
        border-left: 4px solid var(--accent) !important;
        color: var(--accent-hover) !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    /* ========== GLASSMORPHIC SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(244, 244, 245, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 10px;
        border: 2px solid transparent;
        background-clip: content-box;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-hover);
        background-clip: content-box;
    }
    
    /* ========== DATA TABLES ========== */
    .stDataFrame {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    /* ========== REMOVE STREAMLIT BRANDING ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ========== SMOOTH ANIMATIONS ========== */
    * {
        transition: background-color 0.2s ease, border-color 0.2s ease !important;
    }
    </style>
"""
