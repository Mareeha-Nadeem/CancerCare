"""
Network Monitor - Real-time network statistics and monitoring
Demonstrates Computer Networks concepts: Network metrics, Performance monitoring
"""
import psutil
import time
from datetime import datetime
from typing import Dict, List
from collections import deque
import threading

class NetworkMonitor:
    def __init__(self, history_size=100):
        self.history_size = history_size
        self.metrics_history = deque(maxlen=history_size)
        self.active_connections = {}
        self.lock = threading.Lock()
        self.start_time = datetime.utcnow()
    
    def record_connection(self, connection_id: str, client_ip: str, endpoint: str):
        """Record a new active connection"""
        with self.lock:
            self.active_connections[connection_id] = {
                'client_ip': client_ip,
                'endpoint': endpoint,
                'established_at': datetime.utcnow().isoformat(),
                'requests_count': 0
            }
    
    def increment_connection_requests(self, connection_id: str):
        """Increment request count for a connection"""
        with self.lock:
            if connection_id in self.active_connections:
                self.active_connections[connection_id]['requests_count'] += 1
    
    def close_connection(self, connection_id: str):
        """Remove a connection from active connections"""
        with self.lock:
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
    
    def get_system_metrics(self) -> Dict:
        """Get current system network metrics"""
        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # Network I/O
        net_io = psutil.net_io_counters()
        
        # Disk I/O
        disk_io = psutil.disk_io_counters()
        
        metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used_mb': memory.used / (1024 * 1024),
            'memory_available_mb': memory.available / (1024 * 1024),
            'network_bytes_sent': net_io.bytes_sent,
            'network_bytes_recv': net_io.bytes_recv,
            'network_packets_sent': net_io.packets_sent,
            'network_packets_recv': net_io.packets_recv,
            'disk_read_bytes': disk_io.read_bytes if disk_io else 0,
            'disk_write_bytes': disk_io.write_bytes if disk_io else 0,
        }
        
        # Store in history
        with self.lock:
            self.metrics_history.append(metrics)
        
        return metrics
    
    def get_active_connections(self) -> List[Dict]:
        """Get list of active connections"""
        with self.lock:
            return list(self.active_connections.values())
    
    def get_connection_stats(self) -> Dict:
        """Get connection statistics"""
        with self.lock:
            active_count = len(self.active_connections)
            total_requests = sum(
                conn['requests_count'] 
                for conn in self.active_connections.values()
            )
        
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            'active_connections': active_count,
            'total_requests_in_active_connections': total_requests,
            'uptime_seconds': uptime,
            'uptime_formatted': self._format_uptime(uptime)
        }
    
    def get_metrics_history(self, count: int = 50) -> List[Dict]:
        """Get recent metrics history"""
        with self.lock:
            return list(self.metrics_history)[-count:]
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime in human-readable format"""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_network_summary(self) -> Dict:
        """Get comprehensive network summary"""
        system_metrics = self.get_system_metrics()
        connection_stats = self.get_connection_stats()
        
        return {
            'system': system_metrics,
            'connections': connection_stats,
            'active_connections_list': self.get_active_connections()
        }

# Global network monitor instance
network_monitor = NetworkMonitor()
