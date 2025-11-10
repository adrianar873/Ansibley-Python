from pymongo import MongoClient
import psutil
import platform
import socket
from datetime import datetime

class SystemMonitor:
    def __init__(self, mongo_uri, database_name="system_monitor", collection_name="servers_metrics"):
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.hostname = socket.gethostname()
        self._client = None
    
    def _get_mongo_client(self):
        if not self._client:
            self._client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
        return self._client
    
    def close_connection(self):
        if self._client:
            self._client.close()
            self._client = None
    
    def get_system_info(self):
        u = platform.uname()
        return {
            "system": u.system,
            "node_name": u.node,
            "release": u.release,
            "version": u.version,
            "machine": u.machine,
            "processor": u.processor
        }
    
    def get_cpu_info(self):
        freq = psutil.cpu_freq()
        return {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "usage_percent": psutil.cpu_percent(interval=1),
            "frequency": freq._asdict() if freq else None,
            "per_cpu": psutil.cpu_percent(interval=1, percpu=True)
        }
    
    def get_memory_info(self):
        return {
            "virtual": psutil.virtual_memory()._asdict(),
            "swap": psutil.swap_memory()._asdict()
        }
    
    def get_disk_info(self):
        usage = {}
        for p in psutil.disk_partitions():
            try:
                usage[p.mountpoint] = psutil.disk_usage(p.mountpoint)._asdict()
            except PermissionError:
                continue
        return usage
    
    def get_network_info(self):
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        return {
            "interfaces": list(addrs.keys()),
            "addresses": {iface: [a.address for a in addr] for iface, addr in addrs.items()},
            "stats": {iface: s._asdict() for iface, s in stats.items()}
        }
    
    def get_processes(self, limit=10):
        procs = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
            try:
                procs.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return sorted(procs, key=lambda p: p.get('cpu_percent', 0) or 0, reverse=True)[:limit]
    
    def get_all_metrics(self, process_limit=10):
        return {
            "system": self.get_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "processes": self.get_processes(process_limit)
        }
    
    def send_to_mongo(self, data):
        client = self._get_mongo_client()
        collection = client[self.database_name][self.collection_name]
        result = collection.insert_one({
            "host": self.hostname,
            "timestamp": datetime.utcnow(),
            **data
        })
        return result.acknowledged
    
    def send_all_metrics(self, process_limit=10):
        return self.send_to_mongo(self.get_all_metrics(process_limit))
    

