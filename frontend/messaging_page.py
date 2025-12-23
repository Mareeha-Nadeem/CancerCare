"""
Messaging Center - Real-time Chat
Demonstrates Computer Networks point-to-point communication
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.messaging_service import messaging_service

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .msg-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #ff006e;
            margin-bottom: 2rem;
        }
        
        .msg-title {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #ff006e 0%, #ffbe0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .message-sent {
            background: linear-gradient(135deg, #00d9ff 0%, #0088cc 100%);
            padding: 1rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            margin-left: 20%;
            color: white;
        }
        
        .message-received {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #ff006e;
            margin: 0.5rem 0;
            margin-right: 20%;
            color: #e0e0e0;
        }
        
        .conversation-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #ff006e;
            margin: 1rem 0;
            cursor: pointer;
        }
        
        .conversation-card:hover {
            border-color: #ffbe0b;
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="msg-header">
            <h1 class="msg-title">💬 Messaging Center</h1>
            <p style="color: #b0b0b0;">Real-time communication system</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get messaging statistics
    stats = messaging_service.get_statistics()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Messages", stats['total_messages'])
    
    with col2:
        st.metric("Active Conversations", stats['active_conversations'])
    
    with col3:
        st.metric("Data Transferred", f"{stats['kb_transferred']} KB")
    
    with col4:
        st.metric("Unread", messaging_service.get_unread_count("current_user"))
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["💬 Conversations", "📨 New Message", "📊 Statistics"])
    
    with tab1:
        st.subheader("Recent Conversations")
        
        # In a real app, would get user from session
        current_user = "lab_tech"
        
        conversations = messaging_service.get_recent_conversations(current_user, limit=20)
        
        if conversations:
            for conv in conversations:
                with st.container():
                    st.markdown(f"""
                        <div class="conversation-card">
                            <h3 style="color: #ff006e;">👤 {conv['other_user']}</h3>
                            <p>{conv['last_message']}</p>
                            <small style="color: #888;">📅 {conv['last_timestamp']}</small>
                            {f'<span style="background: #ff006e; padding: 0.2rem 0.5rem; border-radius: 5px; color: white; font-size: 0.8rem;">{conv["unread_count"]} unread</span>' if conv['unread_count'] > 0 else ''}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Open Chat with {conv['other_user']}", key=f"chat_{conv['other_user']}"):
                        st.session_state['active_chat'] = conv['other_user']
                        st.rerun()
        else:
            st.info("No conversations yet. Start a new message!")
        
        # Active chat
        if 'active_chat' in st.session_state:
            st.markdown("---")
            st.subheader(f"Chat with {st.session_state['active_chat']}")
            
            # Get conversation
            messages = messaging_service.get_conversation(
                current_user,
                st.session_state['active_chat'],
                limit=50
            )
            
            # Display messages
            for msg in messages:
                if msg['sender'] == current_user:
                    st.markdown(f"""
                        <div class="message-sent">
                            <p>{msg['content']}</p>
                            <small>{msg['timestamp']}</small>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="message-received">
                            <p>{msg['content']}</p>
                            <small>{msg['timestamp']}</small>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Send message form
            with st.form("send_message", clear_on_submit=True):
                message_content = st.text_area("Type your message", key="new_message")
                
                col1, col2 = st.columns([1, 5])
                
                with col1:
                    send_btn = st.form_submit_button("Send 📨")
                
                if send_btn and message_content:
                    messaging_service.send_message(
                        current_user,
                        st.session_state['active_chat'],
                        message_content
                    )
                    st.success("Message sent!")
                    st.rerun()
    
    with tab2:
        st.subheader("Send New Message")
        
        with st.form("new_conversation"):
            recipient = st.selectbox(
                "To:",
                ["doctor_smith", "admin", "patient_john", "tech_emily"]
            )
            
            message = st.text_area("Message")
            
            send = st.form_submit_button("Send Message 📨")
            
            if send and message:
                current_user = "lab_tech"
                
                messaging_service.send_message(
                    current_user,
                    recipient,
                    message
                )
                
                st.success(f"✅ Message sent to {recipient}!")
                st.balloons()
    
    with tab3:
        st.subheader("Messaging Statistics")
        
        st.write("**Network Performance:**")
        st.write(f"- Total Messages Sent: {stats['total_messages']}")
        st.write(f"- Total Bytes Transferred: {stats['total_bytes']:,} bytes")
        st.write(f"- Data Transferred: {stats['kb_transferred']} KB")
        st.write(f"- Active Conversations: {stats['active_conversations']}")
        st.write(f"- Total Conversations: {stats['total_conversations']}")
        
        st.markdown("---")
        
        st.info("""
        **Computer Networks Demonstration:**
        
        This messaging system demonstrates:
        - 📡 Point-to-point communication (client-server model)
        - 📦 Message routing and packet switching
        - 🔗 Connection management
        - 📊 Network performance metrics
        - ⚡ Real-time message delivery
        - 🔄 Asynchronous communication
        """)
    
    # Back button
    st.markdown("---")
    if st.button("⬅️ Back to Home"):
        st.query_params.page = "home"
        st.rerun()
