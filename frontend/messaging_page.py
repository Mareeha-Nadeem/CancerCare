"""
Messaging Page - Threaded Conversations with Read Receipts and System Monitoring
"""
import streamlit as st
from core.services.message_service import message_service
from core.services.system_monitor_service import system_monitor
from core.db_config import get_session
from core.models import User
from datetime import datetime
import time


def show():
    """Advanced messaging with threading, read receipts, and system monitoring"""
    
    st.markdown("""
        <style>
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        .message-card {
            background: var(--bg-surface-elevated); border-radius: 12px; padding: 16px; margin: 12px 0;
            border-left: 4px solid #14B8A6; transition: all 0.2s ease;
        }
        .message-card:hover {
            box-shadow: 0 4px 12px rgba(20, 184, 166, 0.15);
        }
        .message-sent {
            background: #F0FDFA; border-left-color: #0D9488;
        }
        .message-received {
            background: var(--bg-surface-elevated); border-left-color: #14B8A6;
        }
        .unread {
            background: #FFFBEB; border-left-color: #F59E0B; font-weight: 600;
        }
        .read-receipt {
            font-size: 11px; color: #94A3B8; margin-top: 4px;
        }
        .thread-indicator {
            background: #14B8A6; color: white; padding: 2px 8px;
            border-radius: 12px; font-size: 11px; font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Get current user
    user_id = st.session_state.get('user_id', 1)
    
    # Header with messaging center title
    st.markdown("""
        <div class="page-header">
            <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                💬 Messaging Center
            </h1>
            <p style="color: var(--text-muted); margin-top: 8px;">Real-time communication system</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get comprehensive stats
    try:
        msg_stats = message_service.get_stats(user_id)
        conversations = message_service.get_conversations(user_id)
    except Exception as e:
        st.error(f"Error loading messaging data: {str(e)}")
        msg_stats = {
            'total_messages': 0,
            'active_conversations': 0,
            'data_transferred_kb': 0.0,
            'unread_count': 0
        }
        conversations = []
    
    # Get system monitoring stats
    try:
        sys_stats = system_monitor.get_all_stats()
        network = sys_stats['network']
    except Exception:
        sys_stats = {'cpu_usage': 0, 'gpu_usage': 0}
        network = {'incoming_kbps': 0, 'outgoing_kbps': 0}
    
    # Enhanced Stats Display - Messaging + System Monitoring
    st.markdown("### Messaging Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Messages", msg_stats['total_messages'])
    with col2:
        st.metric("Active Conversations", msg_stats['active_conversations'])
    with col3:
        st.metric("Data Transferred", f"{msg_stats['data_transferred_kb']} KB")
    with col4:
        st.metric("Unread", msg_stats['unread_count'])
    
    st.markdown("### 💻 System Monitoring")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("CPU Usage", f"{sys_stats['cpu_usage']:.1f}%")
    with col6:
        st.metric("GPU Usage", f"{sys_stats['gpu_usage']:.1f}%")
    with col7:
        st.metric("Network In", f"{network['incoming_kbps']:.1f} KB/s")
    with col8:
        st.metric("Network Out", f"{network['outgoing_kbps']:.1f} KB/s")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Inbox", "Sent", "Compose"])
    
    with tab1:
        st.markdown("### Conversations")
        
        if conversations:
            for idx, conv in enumerate(conversations):
                try:
                    latest = conv['latest_message']
                    is_unread = conv['unread_count'] > 0 and latest.recipient_id == user_id
                    
                    # Use container for better layout
                    with st.container():
                        # Create two columns for conversation preview
                        col_left, col_right = st.columns([3, 1])
                        
                        with col_left:
                            # Clean conversation label
                            unread_badge = "" if is_unread else ""
                            
                            # Use st.button as clickable conversation item
                            conv_key = f"conv_{idx}"
                            if st.button(
                                f"{unread_badge} **{conv['other_user']}** - {latest.subject[:50]}...",
                                key=conv_key,
                                use_container_width=True
                            ):
                                st.session_state[f'expand_{idx}'] = not st.session_state.get(f'expand_{idx}', False)
                        
                        with col_right:
                            if conv['unread_count'] > 0:
                                st.markdown(f"<span style='color: #F59E0B; font-weight: 600;'>{conv['unread_count']} unread</span>", unsafe_allow_html=True)
                        
                        # Show conversation thread if expanded
                        if st.session_state.get(f'expand_{idx}', False):
                            st.markdown("---")
                            
                            # Load full conversation thread
                            try:
                                thread_messages = message_service.get_conversation(conv['thread_id'])
                            except Exception as e:
                                st.error(f"Error loading conversation: {str(e)}")
                                continue
                            
                            # Display messages in thread
                            for msg in thread_messages:
                                try:
                                    is_sent = msg.sender_id == user_id
                                    msg_class = 'message-sent' if is_sent else 'message-received'
                                    
                                    # Get sender name
                                    sender_name = 'Unknown'
                                    try:
                                        session = get_session()
                                        try:
                                            sender = session.query(User).filter(User.id == msg.sender_id).first()
                                            sender_name = sender.username if sender else 'Unknown'
                                        finally:
                                            session.close()
                                    except Exception:
                                        pass
                                    
                                    # Read receipt icon
                                    read_icon = ""
                                    if is_sent:
                                        if msg.is_read:
                                            read_icon = f"✓✓ Read {msg.read_at.strftime('%I:%M %p')}"
                                        else:
                                            read_icon = f"✓ Delivered {msg.delivered_at.strftime('%I:%M %p')}"
                                    
                                    # Escape HTML in message body to prevent code from showing
                                    import html
                                    clean_body = html.escape(msg.body)
                                    clean_sender = html.escape(sender_name)
                                    
                                    unread_class = 'unread' if not msg.is_read and not is_sent else ''
                                    
                                    # Time formatting
                                    time_str = msg.created_at.strftime('%b %d, %I:%M %p')
                                    
                                    st.markdown(f"""
                                        <div class="message-card {msg_class} {unread_class}">
                                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                                                <div style="font-weight: 600; color: var(--text-main); font-size: 14px;">
                                                    {clean_sender} {'(You)' if is_sent else ''}
                                                </div>
                                                <div style="font-size: 12px; color: #94A3B8;">
                                                    {time_str}
                                                </div>
                                            </div>
                                            <div style="color: #374151; line-height: 1.6; font-size: 14px; white-space: pre-wrap;">
                                                {clean_body}
                                            </div>
                                            {f'<div style="margin-top: 8px; font-size: 11px; color: #10B981;">{read_icon}</div>' if read_icon else ''}
                                        </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Mark as read if viewing
                                    if not is_sent and not msg.is_read:
                                        try:
                                            message_service.mark_as_read(msg.id)
                                        except Exception:
                                            pass
                                except Exception as e:
                                    st.error(f"Error displaying message: {str(e)}")
                            
                            # Reply form
                            st.markdown("**Reply:**")
                            reply_body = st.text_area(
                                "Message",
                                key=f"reply_{conv['thread_id']}",
                                height=100,
                                placeholder="Type your reply..."
                            )
                            
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                if st.button("📤 Send Reply", key=f"send_reply_{conv['thread_id']}"):
                                    if reply_body:
                                        try:
                                            message_service.send_message(
                                                sender_id=user_id,
                                                recipient_id=conv['other_user_id'],
                                                subject=f"Re: {latest.subject}",
                                                body=reply_body,
                                                parent_message_id=latest.id
                                            )
                                            st.success("Reply sent!")
                                            time.sleep(1)
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Failed to send reply: {str(e)}")
                                    else:
                                        st.error("Please enter a message")
                            
                            st.markdown("---")
                        
                except Exception as e:
                    st.error(f"Error loading conversation: {str(e)}")
        else:
            st.info("📭 No conversations yet. Compose a new message!")
    
    with tab2:
        st.markdown("### Sent Messages")
        
        try:
            sent_messages = message_service.get_user_messages(user_id, sent=True)
        except Exception as e:
            st.error(f"Error loading sent messages: {str(e)}")
            sent_messages = []
        
        if sent_messages:
            for msg in sent_messages:
                # Get recipient
                try:
                    session = get_session()
                    try:
                        recipient = session.query(User).filter(User.id == msg.recipient_id).first()
                        recipient_name = recipient.username if recipient else 'Unknown'
                    finally:
                        session.close()
                except Exception:
                    recipient_name = 'Unknown'
                
                # Read status
                read_status = "✓✓ Read" if msg.is_read else "✓ Delivered"
                read_color = "#10B981" if msg.is_read else "#94A3B8"
                
                # Escape HTML
                import html
                clean_body = html.escape(msg.body)
                clean_recipient = html.escape(recipient_name)
                clean_subject = html.escape(msg.subject)
                time_str = msg.created_at.strftime('%b %d, %I:%M %p')
                
                st.markdown(f"""
                    <div class="message-card message-sent">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                            <div style="font-weight: 600; color: var(--text-main); font-size: 14px;">
                                To: {clean_recipient}
                            </div>
                            <div style="font-size: 12px; color: #94A3B8;">
                                {time_str}
                            </div>
                        </div>
                        <div style="font-weight: 500; color: #0D9488; margin-bottom: 8px; font-size: 13px;">
                            {clean_subject}
                        </div>
                        <div style="color: #374151; line-height: 1.6; font-size: 14px; white-space: pre-wrap;">
                            {clean_body[:200]}{'...' if len(msg.body) > 200 else ''}
                        </div>
                        <div style="margin-top: 8px; font-size: 11px; color: {read_color};">
                            {read_status}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No sent messages")
    
    with tab3:
        st.markdown("### Compose New Message")
        
        # Get all users for recipient selection
        try:
            session = get_session()
            try:
                all_users = session.query(User).filter(User.id != user_id).all()
                user_options = {f"{u.username} ({u.email})": u.id for u in all_users}
            finally:
                session.close()
        except Exception as e:
            st.error(f"Error loading users: {str(e)}")
            user_options = {}
        
        if user_options:
            recipient_name = st.selectbox("To:", list(user_options.keys()))
            subject = st.text_input("Subject:", placeholder="Enter subject...")
            priority = st.select_slider("Priority:", options=['low', 'normal', 'high'], value='normal')
            body = st.text_area("Message:", height=200, placeholder="Type your message...")
            
            if st.button("📤 Send Message", use_container_width=True):
                if recipient_name and subject and body:
                    try:
                        recipient_id = user_options[recipient_name]
                        message_service.send_message(
                            sender_id=user_id,
                            recipient_id=recipient_id,
                            subject=subject,
                            body=body,
                            priority=priority
                        )
                        st.success("Message sent successfully!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to send message: {str(e)}")
                else:
                    st.error("Please fill in all fields")
        else:
            st.warning("No other users found. Please run database initialization to create users.")
