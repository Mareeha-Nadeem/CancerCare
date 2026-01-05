"""
Notifications - Modern Design
System notifications and alerts
"""
import streamlit as st
from datetime import datetime


def show():
    """Modern notifications page"""
    
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
                Notifications
            </h1>
            <p style="color: #64748B; margin-top: 8px;">System alerts and updates</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sample notifications
    notifications = [
        {"title": "High Risk Patient Alert", "message": "Patient #1234 requires immediate attention", "type": "error"},
        {"title": "New Lab Results", "message": "Latest scan results available for review", "type": "info"},
        {"title": "Appointment Reminder", "message": "3 appointments scheduled for tomorrow", "type": "warning"},
    ]
    
    for notif in notifications:
        icon = {"error": "⚠️", "info": "ℹ️", "warning": "⚡"}.get(notif['type'], "📢")
        color = {"error": "#EF4444", "info": "#14B8A6", "warning": "#F59E0B"}.get(notif ['type'], "#64748B")
        
        st.markdown(f"""
            <div style="background: white; padding: 16px; border-radius: 12px; margin: 12px 0; 
                 border-left: 4px solid {color};">
                <div style="font-weight: 700; color: #1F2937; margin-bottom: 4px;">
                    {icon} {notif['title']}
                </div>
                <div style="color: #64748B; font-size: 14px;">{notif['message']}</div>
            </div>
        """, unsafe_allow_html=True)
