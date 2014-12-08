import hashlib
import numpy

class data_util(): 
    
    #
    # userid is probably just the requestor's IP because I am lazy
    def get_matrix_hash(self, userid, matrix_name):
        m = hashlib.md5()
        
        print "get_matrix_hash: %s, %s" % (userid, matrix_name)
        
        m.update("%s%s" % (userid, matrix_name))
        
        return m.digest()  
    
    def get_matrices(self, userid):
        
        val = self.ru.r.get(self.get_userid_hash(userid))
        
        val_as_dict = ast.literal_eval(val)
        
        return val
    
    
        
    def get_userid_hash(self, userid):
        m = hashlib.md5()
                    
        m.update("%s" % userid)
        
        return m.digest()
    
    
    def get_md5(self, data):
        
        m = hashlib.md5()
        
        m.update("%s" % data)
        
        return m.digest()
    
    # 
    # Converts a NumPy matrix to a string in the format
    #    '[1.0,2.0,3.0;4.0,5.0,6.0;7.0,8.0,9.0]'
    #
    def matrix_to_string(self, matrix):
        converted = '[%s]' % ';'.join(str(x)[1:-1] for x in matrix.tolist())
        
        print "matrix_to_string.converted = %s" % converted
        
        return converted
        
        
    #
    # Converts a string in the format
    #     '[1.0,2.0,3.0;4.0,5.0,6.0;7.0,8.0,9.0]'
    # to a NumPy matrix
    def string_to_matrix(self, string):
        
#         rows = string[1:-1].split(';')
#         
#         matrix = None
#         for row in rows:
#             
#             arr = numpy.fromstring(row,count=len(row.split(',')),sep=',')
#             
#             print matrix
#             print arr
#             
#             if matrix is not None:
#                 print "NOT FIRST"
#                 matrix = numpy.vstack((matrix, arr))
#             else:
#                 print "FIRST ROW!"
#                 matrix = arr
                
        matrix = numpy.matrix(string)
        print matrix
        print matrix.shape
        
        
        matrix = numpy.matrix(str(matrix.tolist()))
        print matrix.shape
        
        
        return matrix
        
        
    