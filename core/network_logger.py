"""
Network Logger - Tracks all HTTP requests and responses
Demonstrates Computer Networks concepts: HTTP protocol, TCP/IP, logging
"""
import logging
import time
from datetime import datetime
from typing import Dict, Optional
import json
import threading
from collections import deque

class NetworkLogger:
    def __init__(self, max_logs=1000):
        self.max_logs = max_logs
        self.request_logs = deque(maxlen=max_logs)
        self.lock = threading.Lock()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('NetworkLogger')
    
    def log_request(self, 
                   method: str,
                   endpoint: str,
                   client_ip: str,
                   user_agent: Optional[str] = None,
                   request_size: int = 0,
                   **kwargs) -> str:
        """
        Log an incoming HTTP request
        Returns request_id for tracking
        """
        request_id = f"REQ-{int(time.time() * 1000)}"
        
        log_entry = {
            'request_id': request_id,
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'REQUEST',
            'method': method,
            'endpoint': endpoint,
            'client_ip': client_ip,
            'user_agent': user_agent,
            'request_size_bytes': request_size,
            'protocol': 'HTTP/1.1',
            'additional_data': kwargs
        }
        
        with self.lock:
            self.request_logs.append(log_entry)
        
        self.logger.info(f"[REQUEST] {method} {endpoint} from {client_ip}")
        return request_id
    
    def log_response(self,
                    request_id: str,
                    status_code: int,
                    response_size: int = 0,
                    response_time_ms: float = 0,
                    **kwargs):
        """Log an outgoing HTTP response"""
        
        log_entry = {
            'request_id': request_id,
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'RESPONSE',
            'status_code': status_code,
            'response_size_bytes': response_size,
            'response_time_ms': response_time_ms,
            'additional_data': kwargs
        }
        
        with self.lock:
            self.request_logs.append(log_entry)
        
        self.logger.info(
            f"[RESPONSE] {request_id} - Status: {status_code}, "
            f"Size: {response_size}B, Time: {response_time_ms:.2f}ms"
        )
    
    def get_statistics(self) -> Dict:
        """Get network statistics"""
        with self.lock:
            logs = list(self.request_logs)
        
        total_requests = sum(1 for log in logs if log['type'] == 'REQUEST')
        total_responses = sum(1 for log in logs if log['type'] == 'RESPONSE')
        
        # Calculate average response time
        response_times = [
            log['response_time_ms'] 
            for log in logs 
            if log['type'] == 'RESPONSE' and 'response_time_ms' in log
        ]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Status code distribution
        status_codes = {}
        for log in logs:
            if log['type'] == 'RESPONSE':
                code = log.get('status_code', 0)
                status_codes[code] = status_codes.get(code, 0) + 1
        
        # Total data transferred
        total_data_sent = sum(
            log.get('response_size_bytes', 0)
            for log in logs
            if log['type'] == 'RESPONSE'
        )
        
        total_data_received = sum(
            log.get('request_size_bytes', 0)
            for log in logs
            if log['type'] == 'REQUEST'
        )
        
        return {
            'total_requests': total_requests,
            'total_responses': total_responses,
            'avg_response_time_ms': round(avg_response_time, 2),
            'status_code_distribution': status_codes,
            'total_data_sent_bytes': total_data_sent,
            'total_data_received_bytes': total_data_received,
            'total_data_sent_mb': round(total_data_sent / (1024 * 1024), 2),
            'total_data_received_mb': round(total_data_received / (1024 * 1024), 2)
        }
    
    def get_recent_logs(self, count: int = 50) -> list:
        """Get recent log entries"""
        with self.lock:
            return list(self.request_logs)[-count:]
    
    def clear_logs(self):
        """Clear all logs"""
        with self.lock:
            self.request_logs.clear()
        self.logger.info("Logs cleared")

# Global network logger instance
network_logger = NetworkLogger()
