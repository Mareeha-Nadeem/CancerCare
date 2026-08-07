"""
Premium Glassmorphic Theme
Single Color Palette - Medical Teal
Ultra-Modern with Transparency Effects
Inspired by: Apple, Stripe, Linear
"""

"""
Premium International Enterprise Theme
Ultra-Modern, Clean, Elegant SaaS Look
Inspired by top-tier medical and tech enterprise applications
"""

"""
Ultra High-Tech Enterprise Theme
Deep Dark Mode with Glowing Cyber-Medical Accents
Inspired by Palantir, Vercel, and OpenAI's highest-end interfaces
"""

MODERN_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* ========== ULTRA HIGH-TECH COLOR SYSTEM ========== */
    :root {
        /* Primary High-Tech Accents */
        --cyan-glow: #00F0FF;
        --indigo-glow: #7000FF;
        --emerald-glow: #10B981;
        --rose-glow: #F43F5E;
        
        /* Gradients */
        --primary-gradient: linear-gradient(135deg, var(--cyan-glow) 0%, var(--indigo-glow) 100%);
        --text-gradient: linear-gradient(to right, #FFFFFF, #94A3B8);
        
        /* Dark Mode Palette */
        --bg-base: #050505;
        --bg-surface: #0A0A0C;
        --bg-surface-elevated: #121214;
        
        /* Text */
        --text-main: #F8FAFC;
        --text-muted: #94A3B8;
        --text-dark: #475569;
        
        /* Glassmorphism */
        --glass-bg: rgba(18, 18, 20, 0.65);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glass-border-hover: rgba(0, 240, 255, 0.3);
        
        /* Shadows */
        --shadow-glow: 0 0 20px rgba(0, 240, 255, 0.15);
        --shadow-glow-strong: 0 0 30px rgba(0, 240, 255, 0.3);
    }
    
    /* ========== GLOBAL ANIMATED BASE ========== */
    .stApp {
        background-color: var(--bg-base) !important;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(112, 0, 255, 0.04), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(0, 240, 255, 0.04), transparent 25%) !important;
        background-attachment: fixed;
    }
    
    * {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.01em;
        color: var(--text-main);
    }
    
    /* Headings use Space Grotesk for a futuristic, highly engineered look */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        background: var(--text-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        color: var(--text-main) !important;
    }
    
    p, span, div, label {
        color: var(--text-muted) !important;
        line-height: 1.7 !important;
    }
    
    /* Remove default margins */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1400px !important;
    }
    
    /* ========== HIGH-TECH CONTAINERS & ANIMATIONS ========== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.1); }
        50% { box-shadow: 0 0 25px rgba(0, 240, 255, 0.2); }
        100% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.1); }
    }
    
    /* Reset element container */
    .element-container, [data-testid="column"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }
    
    /* Custom Cyber Card Class */
    .premium-card {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-radius: 16px !important;
        border: 1px solid var(--glass-border) !important;
        padding: 30px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        animation: fadeInUp 0.6s ease-out forwards;
        position: relative;
        overflow: hidden;
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px) scale(1.01) !important;
        border-color: var(--glass-border-hover) !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    .premium-card:hover::before {
        opacity: 1;
    }
    
    /* ========== CYBER BUTTONS ========== */
    .stButton > button {
        background: var(--bg-surface-elevated) !important;
        color: var(--cyan-glow) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        background: rgba(0, 240, 255, 0.1) !important;
        border-color: var(--cyan-glow) !important;
        box-shadow: var(--shadow-glow-strong) !important;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.5) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: scale(0.95) !important;
    }
    
    /* Primary Call to Action Button Override */
    .cta-primary {
        background: var(--primary-gradient) !important;
        color: #000 !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(112, 0, 255, 0.4) !important;
    }
    
    .cta-primary:hover {
        background: linear-gradient(135deg, #00FFFF 0%, #8A2BE2 100%) !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.6) !important;
        color: #000 !important;
    }
    
    /* ========== INPUTS & FORMS ========== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        background: var(--bg-surface) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        color: var(--text-main) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus-within,
    .stDateInput > div > div > input:focus {
        border-color: var(--cyan-glow) !important;
        box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.1), 0 0 15px rgba(0, 240, 255, 0.2) !important;
        outline: none !important;
    }
    
    label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        color: var(--text-muted) !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 6px !important;
    }
    
    /* ========== SIDEBAR (COMMAND CENTER) ========== */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 12, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: var(--text-main) !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        background: transparent !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        margin: 4px 0 !important;
        color: var(--text-muted) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        border: 1px solid transparent !important;
        position: relative;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(255, 255, 255, 0.03) !important;
        color: var(--text-main) !important;
        padding-left: 24px !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.1) 0%, transparent 100%) !important;
        color: var(--cyan-glow) !important;
        font-weight: 600 !important;
        border-left: 3px solid var(--cyan-glow) !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    /* ========== HOLOGRAPHIC METRICS ========== */
    [data-testid="stMetric"] {
        background: var(--bg-surface-elevated) !important;
        padding: 24px !important;
        border-radius: 12px !important;
        border: 1px solid var(--glass-border) !important;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5) !important;
        transition: all 0.4s ease !important;
        position: relative !important;
        overflow: hidden !important;
        animation: pulseGlow 4s infinite;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: rgba(0, 240, 255, 0.4) !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 3px; height: 100%;
        background: var(--cyan-glow);
        box-shadow: 0 0 10px var(--cyan-glow);
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 42px !important;
        font-weight: 700 !important;
        background: var(--text-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-top: 8px !important;
        text-shadow: 0 0 20px rgba(255,255,255,0.1) !important;
    }
    
    /* ========== CYBER TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid var(--glass-border) !important;
        padding: 0 !important;
        gap: 32px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-muted) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        padding: 16px 4px !important;
        border-radius: 0 !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.3s ease !important;
        margin-bottom: -1px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-main) !important;
        text-shadow: 0 0 8px rgba(255,255,255,0.3) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: var(--cyan-glow) !important;
        border-bottom: 2px solid var(--cyan-glow) !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 10px -4px var(--cyan-glow) !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.4) !important;
    }
    
    /* ========== EXPANDERS ========== */
    .streamlit-expanderHeader {
        background: var(--bg-surface) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
        padding: 16px 20px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        color: var(--text-main) !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--glass-border-hover) !important;
        background: var(--bg-surface-elevated) !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.05) !important;
    }
    
    /* ========== NEON STATUS MESSAGES ========== */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-left: 4px solid var(--emerald-glow) !important;
        color: #34D399 !important;
        padding: 16px !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.1) !important;
    }
    
    .stError {
        background: rgba(244, 63, 94, 0.1) !important;
        border: 1px solid rgba(244, 63, 94, 0.2) !important;
        border-left: 4px solid var(--rose-glow) !important;
        color: #FDA4AF !important;
        padding: 16px !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(244, 63, 94, 0.1) !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
        border-left: 4px solid #F59E0B !important;
        color: #FCD34D !important;
        padding: 16px !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.1) !important;
    }
    
    .stInfo {
        background: rgba(0, 240, 255, 0.05) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-left: 4px solid var(--cyan-glow) !important;
        color: var(--cyan-glow) !important;
        padding: 16px !important;
        border-radius: 8px !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-base);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--text-dark);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--cyan-glow);
        box-shadow: 0 0 10px var(--cyan-glow);
    }
    
    /* ========== DATA TABLES ========== */
    .stDataFrame {
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }
    
    /* Header row for tables */
    .stDataFrame th {
        background: var(--bg-surface-elevated) !important;
        color: var(--cyan-glow) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stDataFrame td {
        background: var(--bg-surface) !important;
        color: var(--text-muted) !important;
        border-bottom: 1px solid var(--glass-border) !important;
    }
    
    /* ========== STREAMLIT BRANDING ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* ========== UTILITIES & ANIMATIONS ========== */
    .page-header {
        background: linear-gradient(180deg, rgba(18,18,20,0.8) 0%, rgba(10,10,12,0.4) 100%);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 32px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .page-header::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; width: 100%; height: 1px;
        background: linear-gradient(90deg, transparent, var(--cyan-glow), transparent);
        opacity: 0.5;
    }
    
    .page-title {
        font-size: 48px;
        font-weight: 800;
        background: var(--text-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
        text-shadow: 0 0 30px rgba(255,255,255,0.1);
    }
    
    .page-subtitle {
        color: var(--text-muted);
        margin-top: 12px;
        font-size: 18px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* Make images blend nicely */
    img {
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    </style>
"""
