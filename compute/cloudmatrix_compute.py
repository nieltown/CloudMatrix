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
        self.truth = ['t', 'true']
        
        z = zk_util.zk_util('/home/ubuntu/.zk_hosts')
        redis_endpoint = z.get_redis_primary()
        z.client.stop()
        z.client.close()
        
        self.ru = redis_util.redis_util(redis_endpoint)
        self.du = data_util.data_util()
    
    def create(self, operand_list):
        
        print "Computer.create.operand_list: %s" % operand_list
        
        name = operand_list[0]
        data = operand_list[1]

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
        
        # Add the matrix to the user's directory
        userid_hash = self.du.get_userid_hash(self.userid)
        
        keydict = self.ru.r.get(userid_hash)
        
        if keydict:
            keydict = ast.literal_eval(self.ru.r.get(userid_hash))
            keydict['names'] = "%s,%s" % (keydict['names'],name)
        else:
            keydict = {}
            keydict['names'] = name

        self.ru.r.set(userid_hash, keydict)
        
        return 'Compute.create: OK!'
    
    def populate(self):
    
        self.ru.r.delete(self.du.get_userid_hash(self.userid))
        
        self.create(['A','[1,2,3;4,5,6;7,8,9]'])
        self.create(['B','[2,3,4;5,6,7;8,9,10]'])
        
        return 'Populated!'
    
    def list(self):
        
        directory = ast.literal_eval(self.ru.r.get \
                                     (self.du.get_userid_hash(self.userid)))
        
        names = directory['names'].split(',')
        matrices = []
        
        print "***LISTING***"
        for name in names:
            matrix = self.getmatrix(name)
            matrices.append(matrix)
        print "*************"
        
        return matrices
    
    #
    # Operands list should look like this:
    #    ['left', 'right']
    # where 'left' and 'right' are the two matrices you're adding
    def add(self, operand_list, store=False):
        
        print "Computer.add.operand_list: %s" % operand_list
        
        A = self.getmatrix(operand_list[0])
        B = self.getmatrix(operand_list[1])
    
        if len(operand_list) == 3:
            store = operand_list[2].lower()
            print "store = *%s*" % store
    
        sum = numpy.add(numpy.matrix(A['data']), \
                        numpy.matrix(B['data']))
        
        if store in self.truth:
            name = "Sum_%s%s" % (A['name'], B['name'])
            datastring = self.du.matrix_to_string(sum)
            print self.create([name, datastring])
            
        
        print "All summed up"
        
        return sum
    
    #
    # Inverts a matrix.  There is only one operand: the name of the matrix
    # to be inverted 
    def invert(self, operand_list, store=False):
        
        print "Computer.invert.operand_list: %s" % operand_list
        
        A = self.getmatrix(operand_list[0])
        
        if len(operand_list) == 2:
            store = operand_list[1].lower()
            print "store = *%s*" % store
        
        inverse = numpy.linalg.inv(numpy.matrix(A['data']))
        
        if store in self.truth:
            name = "Inverse_%s" % A['name']
            datastring = self.du.matrix_to_string(inverse)
            print self.create([name, datastring])
        
        print "Inverted!"
        
        return inverse
        
    
    #
    # Operands list should look like this:
    #    ['left', 'right']
    # where 'left' and 'right' are the two matrices you're multiplying
    def multiply(self, operand_list, store=False):
        
        print "Computer.multiply.operand_list: %s" % operand_list        
                
        A = self.getmatrix(operand_list[0])
        B = self.getmatrix(operand_list[1])
    
        if len(operand_list) == 3:
            store = operand_list[2].lower()
            print "store = *%s*" % store

        product = numpy.multiply(numpy.matrix(A['data']), \
                             numpy.matrix(B['data']))
        
        if store in self.truth:
            name = "Product_%s%s" % (A['name'], B['name'])
            datastring = self.du.matrix_to_string(product)
            print self.create([name, datastring])
        
        print "Multiplied!"
        
        return product
    
    
    #
    # Retrieves just the data of a matrix structure specified by its name
    def getmatrix(self, name):
        
        print "Gettin that matrix %s" % name
                
        matrix_hash = self.du.get_matrix_hash(self.userid, name)

        val = self.ru.r.get(matrix_hash)

        print "val = %s" % val

        matrix = ast.literal_eval(val)
        
        print "getmatrix.matrix = %s" % matrix
        
        return matrix
    
    #
    # Retrieves a matrix's name by its key
    def getmatrixname(self, key):
        
        data = self.ru.r.get(key)
        
        val = self.ru.r.get(key)
        
        print "getmatrixname.val = %s" % val
        
        data = ast.literal_eval(self.ru.r.get(key))
         
        return data['name']
        
        
            