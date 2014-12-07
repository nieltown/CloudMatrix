from kazoo.client import KazooClient

import random

class zk_util():
    
    def __init__(self, host_file):
         
        host_list = []
         
        z = open(host_file)
         
        for line in z.readlines():
            host = line.replace('\r\n','')
            host_list.append(host)
         
        host_string = ','.join(host_list)
 
        self.client = KazooClient(hosts=host_string)
        self.client.start()
        
    def get_compute_node(self):
        node = self.get_nodes('compute_nodes')
        
        return node
    
    def get_redis_endpoint(self):
        
        node = self.get_nodes('redis_endpoints')
        
        return node
    
    def get_redis_primary(self):
        
        node = self.client.get_children('/%s' % 'redis_endpoints')[0]
        
        return 'cloudmatrixredis-001.c5szdq.0001.use1.cache.amazonaws.com'
    
    def get_nodes(self, node_type):
        
        nodes = self.client.get_children('/%s' % node_type)
        
        node = random.choice(nodes)
        
        return node
        
        
        
        