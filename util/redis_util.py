import hashlib
import redis

class redis_util():
    
    def __init__(self, redis_endpoint, port_num=6379):
        
        self.r = redis.StrictRedis(host=redis_endpoint, port=port_num, db=0)
        
       