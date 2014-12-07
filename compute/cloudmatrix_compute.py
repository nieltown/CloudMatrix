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
        
        print "Listin"
        
        return list
    
    #
    # Operands list should look like this:
    #    ['left', 'right']
    # where 'left' and 'right' are the two matrices you're adding
    def add(self, operand_list):
        
        print "Computer.add.operand_list: %s" % operand_list
        
        matrices = []
        
        for name in operand_list:
            matrices.append(self.getmatrix(name))
                
        sum = numpy.add(matrices[0], matrices[1])
        
        print "All summed up"
        
        return sum
    
    #
    # Operands list should look like this:
    #    ['left', 'right']
    # where 'left' and 'right' are the two matrices you're multiplying
    def multiply(self, operand_list):
        
        print "Computer.add.operand_list: %s" % operand_list
        
        matrices = []
        
        for name in operand_list:
            matrices.append(self.getmatrix(name))
                
        sum = numpy.multiply(matrices[0], matrices[1])
        
        print "All summed up"
        
        return sum
    
    
    #
    # Retrieves just the data of a matrix structure specified by its name
    def getmatrix(self, name):
        
        print "Gettin that matrix"
        
        # Operands come in as a list, so the matrix name is actually the 
        # first element in the parameter 'name'
        name = name[0]
        
        matrix_hash = self.du.get_matrix_hash(self.userid, name)

        matrix = self.ru.r.get(matrix_hash)
        
        matrix = ast.literal_eval(matrix)
        
        
        return numpy.matrix(matrix['data'])
        
        
        
        
        
            