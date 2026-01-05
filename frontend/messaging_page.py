"""
Messages - Modern Design  
Internal messaging system
"""
import streamlit as st
from datetime import datetime


def show():
    """Modern messages page"""
    
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
                Messages
            </h1>
            <p style="color: #64748B; margin-top: 8px;">Team communication</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sample messages
    messages = [
        {"from": "Dr. Johnson", "subject": "Patient Consultation", "preview": "Please review the latest scan results...", "time": "2h ago"},
        {"from": "Lab Tech", "subject": "Equipment Maintenance", "preview": "Scheduled maintenance tomorrow...", "time": "5h ago"},
    ]
    
    for msg in messages:
        st.markdown(f"""
            <div style="background: white; padding: 16px; border-radius: 12px; margin: 12px 0; cursor: pointer;
                 border: 1px solid #E2E8F0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-weight: 700; color: #1F2937;">{msg['from']}</div>
                    <div style="color: #64748B; font-size: 12px;">{msg['time']}</div>
                </div>
                <div style="color: #14B8A6; font-weight: 600; margin-top: 4px;">{msg['subject']}</div>
                <div style="color: #64748B; font-size: 14px; margin-top: 4px;">{msg['preview']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # New message
    with st.form("new_message"):
        st.subheader("✉️ New Message")
        to = st.text_input("To")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        if st.form_submit_button("📤 Send"):
            st.success("✅ Message sent!")
