"""
System Monitoring Service - CPU, GPU, Network tracking
"""
import psutil
import time
from typing import Dict
from datetime import datetime

class SystemMonitorService:
    """Service for tracking system resource usage"""
    
    def __init__(self):
        self.network_last = None
        self.last_check_time = None
    
    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        return psutil.cpu_percent(interval=0.1)
    
    def get_gpu_usage(self) -> float:
        """
        Get GPU usage percentage
        Note: Requires GPU monitoring library (nvidia-smi for NVIDIA)
        Returns 0 if GPU not available
        """
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].load * 100
        except:
            pass
        return 0.0
    
    def get_network_usage(self) -> Dict[str, float]:
        """
        Get network usage (incoming/outgoing in KB/s)
        Returns: {'incoming_kbps': float, 'outgoing_kbps': float}
        """
        current_time = time.time()
        net_io = psutil.net_io_counters()
        
        if self.network_last is None:
            self.network_last = net_io
            self.last_check_time = current_time
            return {'incoming_kbps': 0.0, 'outgoing_kbps': 0.0}
        
        time_delta = current_time - self.last_check_time
        if time_delta == 0:
            return {'incoming_kbps': 0.0, 'outgoing_kbps': 0.0}
        
        bytes_recv_delta = net_io.bytes_recv - self.network_last.bytes_recv
        bytes_sent_delta = net_io.bytes_sent - self.network_last.bytes_sent
        
        incoming_kbps = round((bytes_recv_delta / 1024) / time_delta, 2)
        outgoing_kbps = round((bytes_sent_delta / 1024) / time_delta, 2)
        
        self.network_last = net_io
        self.last_check_time = current_time
        
        return {
            'incoming_kbps': incoming_kbps,
            'outgoing_kbps': outgoing_kbps
        }
    
    def get_all_stats(self) -> Dict:
        """Get all system statistics"""
        return {
            'cpu_usage': self.get_cpu_usage(),
            'gpu_usage': self.get_gpu_usage(),
            'network': self.get_network_usage(),
            'timestamp': datetime.now()
        }


# Global instance
system_monitor = SystemMonitorService()
