"""
Enhanced Notification Service with Real-time Socket Integration
Demonstrates Computer Networks Concepts
"""
import threading
from datetime import datetime
from collections import defaultdict, deque
from typing import Dict, List, Optional

class NotificationService:
    """
    Notification service demonstrating Computer Networks concepts:
    - Message Queue (FIFO)
    - Publish-Subscribe Pattern
    - Asynchronous Communication
    - Network Packet Simulation
    - Message Broadcasting
    """
    
    def __init__(self):
        # Message queue (simulates network packet queue)
        self.notifications = deque(maxlen=1000)
        
        # Subscriber management (pub-sub pattern)
        self.subscribers = defaultdict(list)
        
        # Network statistics
        self.stats = {
            'messages_sent': 0,
            'bytes_transferred': 0,
            'broadcasts': 0,
            'unicast': 0
        }
        
        # Thread lock for concurrent access
        self.lock = threading.Lock()
        
        # Try to import and start socket server
        self.socket_server = None
        try:
            from core.notification_server import notification_server
            self.socket_server = notification_server
            print("✅ Real-time socket server integrated!")
        except Exception as e:
            print(f"⚠️ Socket server not available: {e}")
    
    def send_notification(self, recipient, title, message, notif_type="info"):
        """
        Send notification to specific recipient
        Demonstrates: Unicast transmission
        """
        with self.lock:
            notification = {
                'id': len(self.notifications) + 1,
                'recipient': recipient,
                'title': title,
                'message': message,
                'type': notif_type,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'read': False
            }
            
            self.notifications.append(notification)
            
            # Update network stats
            message_size = len(str(notification).encode('utf-8'))
            self.stats['messages_sent'] += 1
            self.stats['bytes_transferred'] += message_size
            self.stats['unicast'] += 1
            
            # Send via socket server if available (REAL-TIME!)
            if self.socket_server and self.socket_server.running:
                try:
                    self.socket_server.send_to_patient(
                        patient_id=recipient,
                        title=title,
                        message=message,
                        notif_type=notif_type
                    )
                    print(f"📡 Real-time notification sent via socket to {recipient}")
                except Exception as e:
                    print(f"⚠️ Socket send failed: {e}")
            
            return notification
    
    def broadcast(self, title, message, notif_type="info"):
        """
        Broadcast notification to all users
        Demonstrates: Broadcast transmission
        """
        with self.lock:
            notification = {
                'id': len(self.notifications) + 1,
                'recipient': 'all',
                'title': title,
                'message': message,
                'type': notif_type,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'read': False
            }
            
            self.notifications.append(notification)
            
            # Update network stats
            message_size = len(str(notification).encode('utf-8'))
            self.stats['messages_sent'] += 1
            self.stats['bytes_transferred'] += message_size
            self.stats['broadcasts'] += 1
            
            # Broadcast via socket server (REAL-TIME!)
            if self.socket_server and self.socket_server.running:
                try:
                    self.socket_server.broadcast_notification(notification)
                    print(f"📡 Real-time broadcast sent via socket to all clients")
                except Exception as e:
                    print(f"⚠️ Socket broadcast failed: {e}")
            
            return notification
    
    def get_notifications(self, recipient="all", limit=50, unread_only=False):
        """Get notifications for recipient"""
        with self.lock:
            filtered = [
                n for n in self.notifications
                if n['recipient'] in [recipient, 'all']
            ]
            
            if unread_only:
                filtered = [n for n in filtered if not n['read']]
            
            return list(filtered)[-limit:]
    
    def mark_as_read(self, notification_id):
        """Mark notification as read"""
        with self.lock:
            for n in self.notifications:
                if n.get('id') == notification_id:
                    n['read'] = True
                    break
    
    def get_unread_count(self, recipient="all"):
        """Get count of unread notifications"""
        with self.lock:
            count = 0
            for n in self.notifications:
                if n['recipient'] in [recipient, 'all'] and not n['read']:
                    count += 1
            return count
    
    def get_statistics(self):
        """Get network statistics"""
        with self.lock:
            unread = sum(1 for n in self.notifications if not n['read'])
            
            stats = {
                'total_notifications': len(self.notifications),
                'unread_notifications': unread,
                'messages_sent': self.stats['messages_sent'],
                'kb_transferred': round(self.stats['bytes_transferred'] / 1024, 2),
                'broadcasts': self.stats['broadcasts'],
                'unicast': self.stats['unicast']
            }
            
            # Add socket server stats if available
            if self.socket_server and self.socket_server.running:
                socket_stats = self.socket_server.get_stats()
                stats['socket_clients_connected'] = socket_stats['active_clients']
                stats['socket_server_status'] = socket_stats['server_status']
            
            return stats

# Global instance
notification_service = NotificationService()

# Helper functions for common notifications
def notify_new_patient(patient_name, recipient="all"):
    """Notify about new patient registration"""
    return notification_service.send_notification(
        recipient=recipient,
        title="New Patient Registered",
        message=f"Patient {patient_name} has been registered in the system.",
        notif_type="info"
    )

def notify_prediction_complete(patient_name, risk_level, recipient="all"):
    """Notify about prediction completion - REAL-TIME via socket!"""
    notif_type = "error" if risk_level == "High" else "warning" if risk_level == "Medium" else "success"
    
    return notification_service.send_notification(
        recipient=recipient,
        title=f"Risk Assessment Complete: {patient_name}",
        message=f"Cancer risk prediction completed. Risk Level: {risk_level}. Review required.",
        notif_type=notif_type
    )

def notify_appointment_booked(patient_name, appointment_date, recipient="all"):
    """Notify about new appointment - REAL-TIME via socket!"""
    return notification_service.send_notification(
        recipient=recipient,
        title="Appointment Scheduled",
        message=f"New appointment for {patient_name} on {appointment_date}.",
        notif_type="info"
    )

def notify_appointment_reminder(patient_name, appointment_date, recipient):
    """Send appointment reminder to specific patient - REAL-TIME via socket!"""
    return notification_service.send_notification(
        recipient=recipient,
        title="Appointment Reminder",
        message=f"Reminder: You have an appointment on {appointment_date}.",
        notif_type="warning"
    )

def notify_report_uploaded(patient_name, recipient="all"):
    """Notify about report upload"""
    return notification_service.send_notification(
        recipient=recipient,
        title="New Report Uploaded",
        message=f"Medical report uploaded for {patient_name}.",
        notif_type="info"
    )
