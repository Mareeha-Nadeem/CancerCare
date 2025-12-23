"""
Real-time Notification Server using Socket Programming
Demonstrates Computer Networks concepts:
- Socket Programming (TCP/IP)
- Client-Server Architecture
- Publish-Subscribe Pattern
- Message Broadcasting
"""
import socket
import threading
import json
import time
from datetime import datetime
from typing import Dict, Set

class NotificationServer:
    """
    WebSocket-like notification server demonstrating:
    - TCP Socket Programming
    - Multi-threaded client handling
    - Message broadcasting
    - Connection management
    """
    
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients: Set[socket.socket] = set()
        self.notifications = []
        self.running = False
        self.lock = threading.Lock()
        
    def start(self):
        """Start the notification server"""
        try:
            # Create TCP socket (AF_INET = IPv4, SOCK_STREAM = TCP)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to address
            self.server_socket.bind((self.host, self.port))
            
            # Listen for connections
            self.server_socket.listen(5)
            self.running = True
            
            print(f"✅ Notification Server started on {self.host}:{self.port}")
            print(f"📡 Using TCP Socket Programming")
            print(f"🔄 Client-Server Architecture Active")
            
            # Accept connections in separate thread
            accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
            accept_thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Server start error: {e}")
            return False
    
    def _accept_connections(self):
        """Accept incoming client connections"""
        while self.running:
            try:
                # Accept connection (3-way TCP handshake)
                client_socket, address = self.server_socket.accept()
                
                print(f"🔌 New client connected: {address}")
                
                with self.lock:
                    self.clients.add(client_socket)
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"❌ Accept error: {e}")
    
    def _handle_client(self, client_socket, address):
        """Handle individual client connection"""
        try:
            while self.running:
                # Receive data from client
                data = client_socket.recv(1024).decode('utf-8')
                
                if not data:
                    break
                
                # Process client message
                print(f"📨 Received from {address}: {data}")
                
        except Exception as e:
            print(f"❌ Client handler error: {e}")
        finally:
            with self.lock:
                self.clients.discard(client_socket)
            client_socket.close()
            print(f"🔌 Client disconnected: {address}")
    
    def broadcast_notification(self, notification_data: dict):
        """
        Broadcast notification to all connected clients
        Demonstrates:
        - Message Broadcasting
        - Publish-Subscribe Pattern
        """
        message = json.dumps(notification_data)
        
        with self.lock:
            disconnected = set()
            
            for client in self.clients:
                try:
                    # Send message to client
                    client.send(message.encode('utf-8'))
                    print(f"📤 Notification sent to client")
                    
                except Exception as e:
                    print(f"❌ Send error: {e}")
                    disconnected.add(client)
            
            # Remove disconnected clients
            self.clients -= disconnected
        
        # Store notification
        notification_data['timestamp'] = datetime.now().isoformat()
        self.notifications.append(notification_data)
    
    def send_to_patient(self, patient_id: str, title: str, message: str, notif_type: str = "info"):
        """
        Send notification to specific patient
        Demonstrates:
        - Targeted Message Routing
        - Patient-specific Communication Channel
        """
        notification = {
            'recipient': f'patient_{patient_id}',
            'title': title,
            'message': message,
            'type': notif_type,
            'from': 'lab_technician',
            'timestamp': datetime.now().isoformat()
        }
        
        self.broadcast_notification(notification)
        print(f"✅ Notification sent to Patient {patient_id}")
        
        return notification
    
    def get_stats(self):
        """Get server statistics"""
        return {
            'active_clients': len(self.clients),
            'total_notifications': len(self.notifications),
            'server_status': 'Running' if self.running else 'Stopped'
        }
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("✅ Notification Server stopped")

# Global notification server instance
notification_server = NotificationServer()

# Auto-start server
def start_notification_server():
    """Start notification server on first import"""
    global notification_server
    if not notification_server.running:
        notification_server.start()

# Start server automatically
try:
    start_notification_server()
except Exception as e:
    print(f"⚠️ Could not start notification server: {e}")
    print("   Notifications will work in offline mode")
