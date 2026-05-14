"""
Messaging System - Computer Networks Feature
Real-time chat and communication between users
"""
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict, deque
import threading

class Message:
    def __init__(self, sender: str, recipient: str, content: str, message_type: str = "text"):
        self.id = f"msg_{datetime.now().timestamp()}"
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.message_type = message_type  # text, system, alert
        self.timestamp = datetime.now()
        self.read = False
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'recipient': self.recipient,
            'content': self.content,
            'type': self.message_type,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'read': self.read
        }

class MessagingService:
    """
    Messaging system demonstrating Computer Networks:
    - Point-to-point communication
    - Message routing
    - Packet switching concept
    - Connection management
    """
    
    def __init__(self):
        # Store messages by conversation (sender-recipient pair)
        self.conversations = defaultdict(lambda: deque(maxlen=500))
        self.lock = threading.Lock()
        
        # Network statistics
        self.total_messages = 0
        self.total_bytes = 0
        self.active_connections = set()
    
    def send_message(self, sender: str, recipient: str, content: str, message_type: str = "text") -> str:
        """
        Send a message (simulates packet transmission)
        
        Computer Networks Concept: Packet switching and routing
        """
        with self.lock:
            message = Message(sender, recipient, content, message_type)
            
            # Create conversation key (sorted for bidirectional)
            conv_key = self._get_conversation_key(sender, recipient)
            
            # Store message
            self.conversations[conv_key].append(message)
            
            # Update statistics
            self.total_messages += 1
            self.total_bytes += len(content)
            self.active_connections.add(conv_key)
            
            print(f" Message sent from {sender} to {recipient} ({len(content)} bytes)")
            
            return message.id
    
    def get_conversation(self, user1: str, user2: str, limit: int = 50) -> List[Dict]:
        """Get conversation between two users"""
        with self.lock:
            conv_key = self._get_conversation_key(user1, user2)
            messages = list(self.conversations[conv_key])
            
            # Get latest messages
            return [msg.to_dict() for msg in messages[-limit:]]
    
    def get_unread_count(self, user: str) -> int:
        """Get unread message count for user"""
        with self.lock:
            count = 0
            for conv_key, messages in self.conversations.items():
                for msg in messages:
                    if msg.recipient == user and not msg.read:
                        count += 1
            return count
    
    def mark_as_read(self, user: str, other_user: str):
        """Mark all messages in conversation as read"""
        with self.lock:
            conv_key = self._get_conversation_key(user, other_user)
            for msg in self.conversations[conv_key]:
                if msg.recipient == user:
                    msg.read = True
    
    def get_recent_conversations(self, user: str, limit: int = 10) -> List[Dict]:
        """Get user's recent conversations"""
        with self.lock:
            conversations = []
            
            for conv_key, messages in self.conversations.items():
                # Check if user is part of conversation
                if user not in conv_key:
                    continue
                
                if not messages:
                    continue
                
                last_msg = messages[-1]
                other_user = conv_key.replace(user, "").replace("_", "")
                unread = sum(1 for m in messages if m.recipient == user and not m.read)
                
                conversations.append({
                    'other_user': other_user,
                    'last_message': last_msg.content[:50] + "..." if len(last_msg.content) > 50 else last_msg.content,
                    'last_timestamp': last_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'unread_count': unread
                })
            
            # Sort by timestamp
            conversations.sort(key=lambda x: x['last_timestamp'], reverse=True)
            
            return conversations[:limit]
    
    def _get_conversation_key(self, user1: str, user2: str) -> str:
        """Generate consistent conversation key"""
        return "_".join(sorted([user1, user2]))
    
    def get_statistics(self) -> Dict:
        """Get messaging statistics"""
        with self.lock:
            return {
                'total_messages': self.total_messages,
                'total_bytes': self.total_bytes,
                'kb_transferred': round(self.total_bytes / 1024, 2),
                'active_conversations': len(self.active_connections),
                'total_conversations': len(self.conversations)
            }
    
    def broadcast_system_message(self, content: str):
        """Broadcast system message to all"""
        # This would send to all users in a real system
        print(f" System Broadcast: {content}")

# Global messaging service
messaging_service = MessagingService()
