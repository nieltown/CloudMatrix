import ast
import hashlib
import numpy
import redis

import data_util
import redis_util
import zk_util

class Computer():

    def __init__(self, userid):
        self.userid = userid
        
        z = zk_util.zk_util('/home/ubuntu/.zk_hosts')
        redis_endpoint = z.get_redis_primary()
        z.client.stop()
        z.client.close()
        
        self.ru = redis_util.redis_util(redis_endpoint)
        self.du = data_util.data_util()
    
    def list(self, userid):
        
        list = self.get_matrices(userid)
        
        return list
    
    def add(self, operand_list):
        
        sum = 0
        
        print "Computer.add.operand_list: %s" % operand_list
        
        print operand_list
        
        vals = []
        
        for operand in operand_list:
            matrix_hash = self.du.get_matrix_hash(self.userid, operand)

            matrix = self.ru.r.get(matrix_hash)
            
            if matrix:
                vals.append(matrix)
        
        return vals
            