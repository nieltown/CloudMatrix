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
    
    def create(self, operands):
        
        name = operands[0]
        data = operands[1]

        key = self.du.get_matrix_hash(self.userid, name)
        
        matrix = numpy.matrix(data)
        
        value = {}
        value['name'] = name
        value['m'] = matrix.shape[0]
        value['n'] = matrix.shape[1]
        value['data'] = data
        value['type'] = 'matrix'
        value['datamd5'] = self.du.get_md5(data) 
        
        self.ru.r.set(key, str(value))
        
        return 'Compute.create: OK!'
    
    def list(self):
        
        
        
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
                matrix = ast.literal_eval(matrix)
                vals.append(numpy.matrix(matrix['data']))
        
                
        sum = numpy.add(vals[0], vals[1])
        
        return sum
            