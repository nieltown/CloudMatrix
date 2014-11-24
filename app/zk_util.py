from kazoo.client import KazooClient

import random

class zk_util():
    
    def __init__(self, host_string):
        
        self.client = KazooClient(hosts=host_string)
        self.client.start()
        
    def get_compute_node(self):
        node = self.get_nodes('compute_nodes')
        
        return node
    
    def get_redis_endpoint(self):
        
        node = self.get_nodes('redis_endpoints')
        
        return node
    
    def get_nodes(self, node_type):
        
        nodes = self.client.get_children('/%s' % node_type)
        
        node = random.choice(nodes)
        
        return node
        
        
        
        