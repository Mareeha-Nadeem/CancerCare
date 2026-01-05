"""
Messaging Page - Threaded Conversations with Read Receipts
"""
import streamlit as st
from core.services.message_service import message_service
from core.db_config import get_session
from core.models import User
from datetime import datetime
import time


def show():
    """Advanced messaging with threading and read receipts"""
    
    st.markdown("""
        <style>
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        .message-card {
            background: white; border-radius: 12px; padding: 16px; margin: 12px 0;
            border-left: 4px solid #14B8A6; transition: all 0.2s ease;
        }
        .message-card:hover {
            box-shadow: 0 4px 12px rgba(20, 184, 166, 0.15);
        }
        .message-sent {
            background: #F0FDFA; border-left-color: #0D9488;
        }
        .message-received {
            background: white; border-left-color: #14B8A6;
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
    
    # Header
    st.markdown("""
        <div class="page-header">
            <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                💬 Messages
            </h1>
            <p style="color: #64748B; margin-top: 8px;">Threaded conversations with read receipts</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats
    unread_count = message_service.get_unread_count(user_id)
    conversations = message_service.get_conversations(user_id)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💬 Conversations", len(conversations))
    with col2:
        st.metric("📬 Unread", unread_count)
    with col3:
        total_messages = sum(c['message_count'] for c in conversations)
        st.metric("📨 Total Messages", total_messages)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📥 Inbox", "📤 Sent", "✍️ Compose"])
    
    with tab1:
        st.markdown("### Conversations")
        
        if conversations:
            for conv in conversations:
                latest = conv['latest_message']
                is_unread = conv['unread_count'] > 0 and latest.recipient_id == user_id
                
                # Create clean expander label
                unread_badge = "🔴 " if is_unread else ""
                expander_label = f"{unread_badge}{conv['other_user']}: {latest.subject}"
                if conv['unread_count'] > 0:
                    expander_label += f" ({conv['unread_count']} unread)"
                
                with st.expander(expander_label, expanded=False):
                    # Load full conversation thread
                    thread_messages = message_service.get_conversation(conv['thread_id'])
                    
                    # Display messages in thread
                    for msg in thread_messages:
                        is_sent = msg.sender_id == user_id
                        msg_class = 'message-sent' if is_sent else 'message-received'
                        
                        # Get sender name
                        session = get_session()
                        try:
                            sender = session.query(User).filter(User.id == msg.sender_id).first()
                            sender_name = sender.username if sender else 'Unknown'
                        finally:
                            session.close()
                        
                        # Read receipt icon
                        read_icon = ""
                        if is_sent:
                            if msg.is_read:
                                read_icon = f"✓✓ Read {msg.read_at.strftime('%I:%M %p')}"
                            else:
                                read_icon = f"✓ Delivered {msg.delivered_at.strftime('%I:%M %p')}"
                        
                        st.markdown(f"""
                            <div class="message-card {msg_class} {unread_class if not msg.is_read and not is_sent else ''}">
                                <div style="font-weight: 700; color: #1F2937;">
                                    {sender_name} {'(You)' if is_sent else ''}
                                    {f'<span class="thread-indicator">Reply</span>' if msg.parent_message_id else ''}
                                </div>
                                <div style="color: #64748B; margin-top: 8px; font-size: 14px;">
                                    {msg.body}
                                </div>
                                <div class="read-receipt">
                                    {msg.created_at.strftime('%B %d, %Y at %I:%M %p')}
                                    {f' • {read_icon}' if read_icon else ''}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Mark as read if viewing
                        if not is_sent and not msg.is_read:
                            message_service.mark_as_read(msg.id)
                    
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
                                # Send reply
                                message_service.send_message(
                                    sender_id=user_id,
                                    recipient_id=conv['other_user_id'],
                                    subject=f"Re: {latest.subject}",
                                    body=reply_body,
                                    parent_message_id=latest.id
                                )
                                st.success("✅ Reply sent!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("⚠️ Please enter a message")
        else:
            st.info("📭 No conversations yet. Compose a new message!")
    
    with tab2:
        st.markdown("### Sent Messages")
        sent_messages = message_service.get_user_messages(user_id, sent=True)
        
        if sent_messages:
            for msg in sent_messages:
                # Get recipient
                session = get_session()
                try:
                    recipient = session.query(User).filter(User.id == msg.recipient_id).first()
                    recipient_name = recipient.username if recipient else 'Unknown'
                finally:
                    session.close()
                
                # Read status
                read_status = "✓✓ Read" if msg.is_read else "✓ Delivered"
                read_color = "#10B981" if msg.is_read else "#94A3B8"
                
                st.markdown(f"""
                    <div class="message-card message-sent">
                        <div style="font-weight: 700; color: #1F2937;">
                            To: {recipient_name} • {msg.subject}
                        </div>
                        <div style="color: #64748B; margin-top: 8px;">
                            {msg.body[:150]}{'...' if len(msg.body) > 150 else ''}
                        </div>
                        <div class="read-receipt">
                            {msg.created_at.strftime('%B %d, %Y at %I:%M %p')}
                            <span style="color: {read_color}; margin-left: 12px;">{read_status}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No sent messages")
    
    with tab3:
        st.markdown("### Compose New Message")
        
        # Get all users for recipient selection
        session = get_session()
        try:
            all_users = session.query(User).filter(User.id != user_id).all()
            user_options = {f"{u.username} ({u.email})": u.id for u in all_users}
        finally:
            session.close()
        
        if user_options:
            recipient_name = st.selectbox("To:", list(user_options.keys()))
            subject = st.text_input("Subject:", placeholder="Enter subject...")
            priority = st.select_slider("Priority:", options=['low', 'normal', 'high'], value='normal')
            body = st.text_area("Message:", height=200, placeholder="Type your message...")
            
            if st.button("📤 Send Message", use_container_width=True):
                if recipient_name and subject and body:
                    recipient_id = user_options[recipient_name]
                    message_service.send_message(
                        sender_id=user_id,
                        recipient_id=recipient_id,
                        subject=subject,
                        body=body,
                        priority=priority
                    )
                    st.success("✅ Message sent successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all fields")
        else:
            st.warning("No other users found in the system")
