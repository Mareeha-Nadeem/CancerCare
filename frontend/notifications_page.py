"""
Notifications Page - Real-time with Priority Queue & Auto-refresh
"""
import streamlit as st
from core.notification_service import notification_service
from datetime import datetime
import time


def show():
    """Advanced notifications with real-time updates"""
    
    st.markdown("""
        <style>
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        .notification-card {
            background: white; border-radius: 12px; padding: 16px; margin: 12px 0;
            border-left: 4px solid; transition: all 0.2s ease;
        }
        .notification-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .urgent {border-left-color: #DC2626 !important; background: #FEF2F2 !important;}
        .high {border-left-color: #F59E0B !important; background: #FFFBEB !important;}
        .normal {border-left-color: #14B8A6 !important;}
        .low {border-left-color: #94A3B8 !important;}
        .read {opacity: 0.6;}
        .badge {
            display: inline-block; padding: 4px 12px; border-radius: 12px;
            font-size: 12px; font-weight: 600; margin-left: 8px;
        }
        .badge-urgent {background: #DC2626; color: white;}
        .badge-high {background: #F59E0B; color: white;}
        .badge-normal {background: #14B8A6; color: white;}
        .badge-low {background: #94A3B8; color: white;}
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for auto-refresh
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    # Get current user (defaulting to user_id=1 for demo)
    user_id = st.session_state.get('user_id', 1)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
            <div class="page-header">
                <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                    🔔 Notifications
                </h1>
                <p style="color: #64748B; margin-top: 8px;">Real-time notification stream with priority queue</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Auto-refresh toggle
        auto_refresh = st.checkbox("⚡ Auto-refresh (5s)", value=True)
    
    # Priority stats
    stats = notification_service.get_priority_stats(user_id)
    unread_count = notification_service.get_unread_count(user_id)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Unread", unread_count)
    with col2:
        st.metric("🔴 Urgent", stats.get('urgent', 0))
    with col3:
        st.metric("🟠 High", stats.get('high', 0))
    with col4:
        st.metric("🟢 Normal", stats.get('normal', 0))
    with col5:
        st.metric("⚪ Low", stats.get('low', 0))
    
    # Filters
    st.markdown("### Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_unread_only = st.checkbox("📬 Unread only", value=False)
    with col2:
        priority_filter = st.selectbox("Priority", [None, "urgent", "high", "normal", "low"])
    with col3:
        type_filter = st.selectbox("Type", [None, "info", "warning", "error", "success"])
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 2, 6])
    with col1:
        if st.button("✅ Mark All Read", use_container_width=True):
            notification_service.mark_all_as_read(user_id)
            st.rerun()
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Get notifications (priority queue sorted)
    notifications = notification_service.get_user_notifications(
        user_id=user_id,
        unread_only=show_unread_only,
        priority_filter=priority_filter,
        type_filter=type_filter
    )
    
    st.markdown("---")
    st.markdown(f"### 📊 {len(notifications)} Notifications")
    
    # Display notifications
    if notifications:
        for notif in notifications:
            read_class = 'read' if notif.is_read else ''
            priority_class = notif.priority
            
            # Icon based on type
            icon = {
                'info': 'ℹ️',
                'warning': '⚠️',
                'error': '❌',
                'success': '✅'
            }.get(notif.type, 'ℹ️')
            
            # Badge color
            badge_class = f"badge-{notif.priority}"
            
            st.markdown(f"""
                <div class="notification-card {priority_class} {read_class}">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <div style="font-weight: 700; font-size: 16px; color: #1F2937;">
                                {icon} {notif.title}
                                <span class="badge {badge_class}">{notif.priority.upper()}</span>
                            </div>
                            <div style="color: #64748B; margin-top: 8px;">
                                {notif.message}
                            </div>
                            <div style="color: #94A3B8; font-size: 12px; margin-top: 8px;">
                                {notif.created_at.strftime('%B %d, %Y at %I:%M %p')}
                                {f' • Read {notif.read_at.strftime("%I:%M %p")}' if notif.is_read else ''}
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Action buttons for each notification
            col1, col2,  col3 = st.columns([2, 2, 6])
            with col1:
                if not notif.is_read:
                    if st.button("✓ Mark Read", key=f"read_{notif.id}"):
                        notification_service.mark_as_read(notif.id)
                        st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_{notif.id}"):
                    notification_service.delete_notification(notif.id)
                    st.rerun()
    else:
        st.info("📭 No notifications to display")
    
    # Auto-refresh logic
    if auto_refresh:
        current_time = time.time()
        if current_time - st.session_state.last_refresh > 5:  # 5 seconds
            st.session_state.last_refresh = current_time
            st.rerun()
        
        # Show countdown
        time_since_refresh = int(current_time - st.session_state.last_refresh)
        refresh_in = max(0, 5 - time_since_refresh)
        st.sidebar.info(f"⏱️ Refreshing in {refresh_in}s...")
        time.sleep(1)
        st.rerun()
