import numpy
import redis

import redis_util
import zk_util

class Computer():

    def __init__(self, ip):
        self.ip = ip
        
        z = zk_util.zk_util('/home/ubuntu/.zk_hosts')
        redis_endpoint = z.get_redis_primary()
        
        self.ru = redis_util.redis_util(redis_endpoint)
        
    
    def add(self, operand_list):
        
        print "Computer.add.operand_list: %s" % operand_list
        
        return str(operand_list)
        
        vals = []
        
        for operand in operand_list:
            matrix_hash = self.ru.get_matrix_hash(ip, operand)
            print matrix_hash
            vals.append(self.ru.get(matrx_hash)
    
    
    
    