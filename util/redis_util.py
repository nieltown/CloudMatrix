import hashlib
import redis

class redis_util():
    
    def __init__(self, redis_endpoint, port_num=6379):
        
        self.r = redis.StrictRedis(host=redis_endpoint, port=port_num, db=0)
        
    #
    # userid is probably just the requestor's IP because I am lazy
    def get_matrix_hash(self, userid, matrix_name):
        m = hashlib.md5()
                    
        m.update("%s%s" % (userid, matrix_name))
        
        return m.digest()  