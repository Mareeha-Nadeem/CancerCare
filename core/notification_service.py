"""
Notification Service - Real-time notifications with priority queue
"""
from core.db_config import get_session
from core.models import Notification
from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy import desc


class NotificationService:
    """Service for managing notifications with priority queue"""
    
    @staticmethod
    def create_notification(
        user_id: int,
        title: str,
        message: str,
        notification_type: str = 'info',
        priority: str = 'normal',
        link: str = None,
        related_id: int = None,
        related_type: str = None
    ) -> Notification:
        """
        Create a new notification
        
        Priority levels: low, normal, high, urgent
        Types: info, warning, error, success
        """
        session = get_session()
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                type=notification_type,
                priority=priority,
                link=link,
                related_id=related_id,
                related_type=related_type
            )
            session.add(notification)
            session.commit()
            session.refresh(notification)
            return notification
        finally:
            session.close()
    
    @staticmethod
    def get_user_notifications(
        user_id: int,
        unread_only: bool = False,
        priority_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        limit: int = 100
    ) -> List[Notification]:
        """Get notifications for a user with filters (priority queue)"""
        session = get_session()
        try:
            query = session.query(Notification).filter(Notification.user_id == user_id)
            
            if unread_only:
                query = query.filter(Notification.is_read == False)
            
            if priority_filter:
                query = query.filter(Notification.priority == priority_filter)
            
            if type_filter:
                query = query.filter(Notification.type == type_filter)
            
            # Priority queue: urgent > high > normal > low, then by created_at desc
            priority_order = {
                'urgent': 0,
                'high': 1,
                'normal': 2,
                'low': 3
            }
            
            notifications = query.order_by(desc(Notification.created_at)).limit(limit).all()
            
            # Sort by priority first, then by created_at
            notifications.sort(key=lambda n: (priority_order.get(n.priority, 2), -n.created_at.timestamp()))
            
            return notifications
        finally:
            session.close()
    
    @staticmethod
    def mark_as_read(notification_id: int) -> bool:
        """Mark notification as read"""
        session = get_session()
        try:
            notification = session.query(Notification).filter(Notification.id == notification_id).first()
            if notification:
                notification.is_read = True
                notification.read_at = datetime.utcnow()
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    @staticmethod
    def mark_all_as_read(user_id: int) -> int:
        """Mark all notifications as read for a user"""
        session = get_session()
        try:
            count = session.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
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
        """Get count of unread notifications"""
        session = get_session()
        try:
            return session.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).count()
        finally:
            session.close()
    
    @staticmethod
    def delete_notification(notification_id: int) -> bool:
        """Delete a notification"""
        session = get_session()
        try:
            notification = session.query(Notification).filter(Notification.id == notification_id).first()
            if notification:
                session.delete(notification)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    @staticmethod
    def get_priority_stats(user_id: int) -> Dict[str, int]:
        """Get notification counts by priority"""
        session = get_session()
        try:
            notifications = session.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).all()
            
            stats = {'urgent': 0, 'high': 0, 'normal': 0, 'low': 0}
            for notif in notifications:
                stats[notif.priority] = stats.get(notif.priority, 0) + 1
            
            return stats
        finally:
            session.close()


# Global instance
notification_service = NotificationService()
