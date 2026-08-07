"""
Authentication Page
Login and Signup forms
"""
import streamlit as st
from core.services.auth_service import auth_service


def show():
    """Display authentication page (login/signup)"""
    
    # Custom CSS
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1e7e8c 0%, #2c9db0 100%);
        }
        
        .auth-container {
            background: var(--bg-surface-elevated);
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 500px;
            margin: 50px auto;
        }
        
        .auth-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .auth-header h1 {
            color: #1e7e8c;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .auth-header p {
            color: #666;
            font-size: 1.1rem;
        }
        
        .stButton > button {
            background: #1e7e8c;
            color: white;
            border: none;
            padding: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 8px;
            width: 100%;
            margin-top: 20px;
        }
        
        .stButton > button:hover {
            background: #2c9db0;
        }
        
        .toggle-link {
            text-align: center;
            margin-top: 20px;
            color: #666;
        }
        
        .toggle-link a {
            color: #1e7e8c;
            font-weight: 600;
            text-decoration: none;
        }
        
        .back-button {
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Back to landing page button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
    
    # Get auth mode from session state
    mode = st.session_state.get('auth_mode', 'login')
    
    # Container for form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if mode == 'login':
            show_login_form()
        else:
            show_signup_form()


def show_login_form():
    """Display login form"""
    st.markdown("""
        <div class="auth-header">
            <h1>Login</h1>
            <p>Access your CancerCare dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("Please fill in all fields")
            else:
                # Attempt login
                user, error = auth_service.login_user(username, password)
                
                if error:
                    st.error(f" {error}")
                else:
                    # Set session state
                    st.session_state.authenticated = True
                    st.session_state.user_id = user['id']
                    st.session_state.username = user['username']
                    st.session_state.user_role = user['role']
                    st.session_state.page = "lab_dashboard"
                    
                    st.success(f"Welcome back, {user['username']}!")
                    st.rerun()
    
    # Toggle to signup
    st.markdown("""
        <div class="toggle-link">
            Don't have an account? 
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Sign Up Here", use_container_width=True):
        st.session_state.auth_mode = "signup"
        st.rerun()


def show_signup_form():
    """Display signup form"""
    st.markdown("""
        <div class="auth-header">
            <h1>Sign Up</h1>
            <p>Create your CancerCare account</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form", clear_on_submit=False):
        username = st.text_input(
            "Username",
            placeholder="Choose a username",
            help="Unique username for login",
            key="signup_username"
        )
        
        email = st.text_input(
            "Email",
            placeholder="your.email@example.com",
            key="signup_email"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Choose a strong password",
            help="Minimum 6 characters",
            key="signup_password"
        )
        
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="signup_confirm"
        )
        
        role = st.selectbox(
            "Role",
            options=["lab_tech", "doctor"],
            help="Select your role. Admin accounts are created by administrators only."
        )
        
        submit = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit:
            # Validation
            if not username or not email or not password or not confirm_password:
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error(" Passwords do not match")
            elif len(password) < 6:
                st.error(" Password must be at least 6 characters")
            elif "@" not in email or "." not in email:
                st.error(" Please enter a valid email address")
            else:
                # Attempt registration
                user, error = auth_service.register_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role
                )
                
                if error:
                    st.error(f" {error}")
                else:
                    # Auto-login after signup
                    st.session_state.authenticated = True
                    st.session_state.user_id = user['id']
                    st.session_state.username = user['username']
                    st.session_state.user_role = user['role']
                    st.session_state.page = "lab_dashboard"
                    
                    st.success(f"Account created successfully! Welcome, {user['username']}!")
                    st.balloons()
                    st.rerun()
    
    # Toggle to login
    st.markdown("""
        <div class="toggle-link">
            Already have an account?
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Login Here", use_container_width=True):
        st.session_state.auth_mode = "login"
        st.rerun()
