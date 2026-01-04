# CancerCare - Contact Page
import streamlit as st

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .contact-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid #00d9ff;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title(" Contact Us")
    
    st.markdown("""
    <div class="contact-card">
        <h3 style="color: #00d9ff;">Get in Touch</h3>
        <p>For inquiries about this project, please contact:</p>
        <ul>
            <li><strong>Project:</strong> CancerCare Lung Cancer Risk Prediction System</li>
            <li><strong>Email:</strong> support@cancercare.edu</li>
            <li><strong>GitHub:</strong> github.com/cancercare</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Send a Message")
    
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        
        if st.form_submit_button("Send Message"):
            if name and email and message:
                st.success(" Message sent! We'll get back to you soon.")
            else:
                st.error("Please fill in all fields")
    
    if st.button(" Back to Home"):
        st.query_params.page = "home"
        st.rerun()