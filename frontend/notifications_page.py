"""
Notifications Center - Live Updates Page
Demonstrates Computer Networks real-time communication
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.notification_service import notification_service

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .notif-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #00d9ff;
            margin-bottom: 2rem;
        }
        
        .notif-title {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .notif-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #00d9ff;
            margin: 1rem 0;
        }
        
        .notif-success {
            border-left: 4px solid #00ff88;
        }
        
        .notif-warning {
            border-left: 4px solid #ffbe0b;
        }
        
        .notif-error {
            border-left: 4px solid #ff006e;
        }
        
        .notif-info {
            border-left: 4px solid #00d9ff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="notif-header">
            <h1 class="notif-title">🔔 Live Notifications</h1>
            <p style="color: #b0b0b0;">Real-time system updates and alerts</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh toggle
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        auto_refresh = st.checkbox("Auto-refresh", value=False)
    
    with col3:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Get statistics
    stats = notification_service.get_statistics()
    
    # Display metrics
    st.markdown("## 📊 Notification Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Notifications", stats['total_notifications'])
    
    with col2:
        st.metric("Unread", stats['unread_notifications'])
    
    with col3:
        st.metric("Messages Sent", stats['messages_sent'])
    
    with col4:
        st.metric("Data Transferred", f"{stats['kb_transferred']} KB")
    
    st.markdown("---")
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        filter_type = st.selectbox(
            "Filter by Type",
            ["All", "Info", "Success", "Warning", "Error"]
        )
    
    with col2:
        show_unread_only = st.checkbox("Unread only", value=False)
    
    # Get notifications
    notifications = notification_service.get_notifications(
        recipient="all",
        limit=50,
        unread_only=show_unread_only
    )
    
    # Filter by type
    if filter_type != "All":
        notifications = [n for n in notifications if n['type'].lower() == filter_type.lower()]
    
    # Display notifications
    st.markdown("## 📬 Recent Notifications")
    
    if notifications:
        for notif in notifications:
            notif_type = notif['type']
            icon_map = {
                'info': '💡',
                'success': '✅',
                'warning': '⚠️',
                'error': '❌'
            }
            
            icon = icon_map.get(notif_type, '📌')
            
            with st.container():
                st.markdown(f"""
                    <div class="notif-card notif-{notif_type}">
                        <h3 style="color: #00d9ff;">{icon} {notif['title']}</h3>
                        <p>{notif['message']}</p>
                        <small style="color: #888;">📅 {notif['timestamp']}</small>
                    </div>
                """, unsafe_allow_html=True)
        
        # Mark all as read button
        if st.button("✅ Mark All as Read"):
            # In a real app, would mark notifications as read
            st.success("All notifications marked as read!")
            st.rerun()
    
    else:
        st.info("No notifications to display")
    
    # Auto-refresh implementation
    if auto_refresh:
        import time
        time.sleep(5)
        st.rerun()
    
    # Back button
    st.markdown("---")
    if st.button("⬅️ Back to Home"):
        st.query_params.page = "home"
        st.rerun()
