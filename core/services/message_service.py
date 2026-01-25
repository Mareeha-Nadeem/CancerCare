"""
Message Service - Threaded messaging with read receipts
"""
from core.db_config import get_session
from core.models import Message, User
from datetime import datetime
from typing import List, Optional, Dict, Tuple
from sqlalchemy import or_, and_, desc
import uuid


class MessageService:
    """Service for managing threaded messages with read receipts"""
    
    @staticmethod
    def send_message(
        sender_id: int,
        recipient_id: int,
        subject: str,
        body: str,
        priority: str = 'normal',
        parent_message_id: Optional[int] = None
    ) -> Message:
        """
        Send a new message
        
        If parent_message_id is provided, creates a threaded reply
        """
        session = get_session()
        try:
            # Generate thread_id if this is a new conversation
            thread_id = None
            if parent_message_id:
                # Get parent message to use its thread_id
                parent = session.query(Message).filter(Message.id == parent_message_id).first()
                if parent:
                    thread_id = parent.thread_id or str(parent.id)
            else:
                # New conversation - generate new thread_id
                thread_id = str(uuid.uuid4())
            
            message = Message(
                sender_id=sender_id,
                recipient_id=recipient_id,
                subject=subject,
                body=body,
                priority=priority,
                thread_id=thread_id,
                parent_message_id=parent_message_id,
                delivered_at=datetime.utcnow()
            )
            
            session.add(message)
            session.commit()
            session.refresh(message)
            return message
        finally:
            session.close()
    
    @staticmethod
    def get_user_messages(
        user_id: int,
        unread_only: bool = False,
        sent: bool = False
    ) -> List[Message]:
        """Get messages for a user (inbox or sent)"""
        session = get_session()
        try:
            if sent:
                query = session.query(Message).filter(
                    Message.sender_id == user_id,
                    Message.is_deleted == False
                )
            else:
                query = session.query(Message).filter(
                    Message.recipient_id == user_id,
                    Message.is_deleted == False
                )
            
            if unread_only:
                query = query.filter(Message.is_read == False)
            
            return query.order_by(desc(Message.created_at)).all()
        finally:
            session.close()
    
    @staticmethod
    def get_conversation(thread_id: str) -> List[Message]:
        """Get all messages in a thread (conversation)"""
        session = get_session()
        try:
            messages = session.query(Message).filter(
                Message.thread_id == thread_id,
                Message.is_deleted == False
            ).order_by(Message.created_at).all()
            
            return messages
        finally:
            session.close()
    
    @staticmethod
    def get_conversations(user_id: int) -> List[Dict]:
        """
        Get all conversations for a user (grouped by thread)
        Returns list of dicts with latest message per thread
        """
        session = get_session()
        try:
            # Get all messages where user is sender or recipient
            messages = session.query(Message).filter(
                or_(
                    Message.sender_id == user_id,
                    Message.recipient_id == user_id
                ),
                Message.is_deleted == False
            ).order_by(desc(Message.created_at)).all()
            
            # Group by thread_id
            threads = {}
            for msg in messages:
                thread_key = msg.thread_id or str(msg.id)
                if thread_key not in threads:
                    # Get other participant
                    other_user_id = msg.recipient_id if msg.sender_id == user_id else msg.sender_id
                    other_user = session.query(User).filter(User.id == other_user_id).first()
                    
                    # Count unread messages in thread
                    unread_count = sum(
                        1 for m in messages 
                        if (m.thread_id == thread_key or str(m.id) == thread_key)
                        and m.recipient_id == user_id
                        and not m.is_read
                    )
                    
                    threads[thread_key] = {
                        'thread_id': thread_key,
                        'latest_message': msg,
                        'other_user': other_user.username if other_user else 'Unknown',
                        'other_user_id': other_user_id,
                        'unread_count': unread_count,
                        'message_count': sum(1 for m in messages if (m.thread_id == thread_key or str(m.id) == thread_key))
                    }
            
            # Sort by latest message
            return sorted(threads.values(), key=lambda x: x['latest_message'].created_at, reverse=True)
        finally:
            session.close()
    
    @staticmethod
    def mark_as_read(message_id: int) -> Tuple[bool, Optional[datetime]]:
        """Mark message as read, returns (success, read_at)"""
        session = get_session()
        try:
            message = session.query(Message).filter(Message.id == message_id).first()
            if message:
                message.is_read = True
                message.read_at = datetime.utcnow()
                session.commit()
                return True, message.read_at
            return False, None
        finally:
            session.close()
    
    @staticmethod
    def mark_thread_as_read(thread_id: str, user_id: int) -> int:
        """Mark all messages in a thread as read for a user"""
        session = get_session()
        try:
            count = session.query(Message).filter(
                Message.thread_id == thread_id,
                Message.recipient_id == user_id,
                Message.is_read == False
            ).update({
                'is_read': True,
                'read_at': datetime.utcnow()
            })
            session.commit()
            return count
        finally:
            session.close()
    
    @staticmethod
    def get_unread_count(user_id: int) -> int:
        """Get count of unread messages"""
        session = get_session()
        try:
            return session.query(Message).filter(
                Message.recipient_id == user_id,
                Message.is_read == False,
                Message.is_deleted == False
            ).count()
        finally:
            session.close()
    
    @staticmethod
    def delete_message(message_id: int, hard_delete: bool = False) -> bool:
        """Delete a message (soft or hard delete)"""
        session = get_session()
        try:
            message = session.query(Message).filter(Message.id == message_id).first()
            if message:
                if hard_delete:
                    session.delete(message)
                else:
                    message.is_deleted = True
                    message.deleted_at = datetime.utcnow()
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    @staticmethod
    def search_messages(user_id: int, search_term: str) -> List[Message]:
        """Search messages by subject or body"""
        session = get_session()
        try:
            search = f"%{search_term}%"
            return session.query(Message).filter(
                or_(
                    Message.sender_id == user_id,
                    Message.recipient_id == user_id
                ),
                Message.is_deleted == False,
                or_(
                    Message.subject.like(search),
                    Message.body.like(search)
                )
            ).order_by(desc(Message.created_at)).all()
        finally:
            session.close()
    
    @staticmethod
    def get_stats(user_id: int) -> Dict:
        """
        Get comprehensive messaging statistics for a user
        Returns: {
            'total_messages': int,
            'active_conversations': int,
            'data_transferred_kb': float,
            'unread_count': int
        }
        """
        session = get_session()
        try:
            # Total messages (sent + received)
            total_sent = session.query(Message).filter(
                Message.sender_id == user_id,
                Message.is_deleted == False
            ).count()
            
            total_received = session.query(Message).filter(
                Message.recipient_id == user_id,
                Message.is_deleted == False
            ).count()
            
            total_messages = total_sent + total_received
            
            # Active conversations (unique threads)
            messages = session.query(Message).filter(
                or_(
                    Message.sender_id == user_id,
                    Message.recipient_id == user_id
                ),
                Message.is_deleted == False
            ).all()
            
            unique_threads = set()
            for msg in messages:
                thread_key = msg.thread_id or str(msg.id)
                unique_threads.add(thread_key)
            
            active_conversations = len(unique_threads)
            
            # Data transferred (approximate size in KB)
            data_size = 0
            for msg in messages:
                # Approximate: subject + body length in bytes
                msg_size = len(msg.subject.encode('utf-8')) + len(msg.body.encode('utf-8'))
                data_size += msg_size
            
            data_transferred_kb = round(data_size / 1024, 2)
            
            # Unread count
            unread_count = session.query(Message).filter(
                Message.recipient_id == user_id,
                Message.is_read == False,
                Message.is_deleted == False
            ).count()
            
            return {
                'total_messages': total_messages,
                'active_conversations': active_conversations,
                'data_transferred_kb': data_transferred_kb,
                'unread_count': unread_count
            }
        finally:
            session.close()


# Global instance
message_service = MessageService()
