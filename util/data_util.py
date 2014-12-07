import hashlib
    
class data_util(): 
    
    #
    # userid is probably just the requestor's IP because I am lazy
    def get_matrix_hash(self, userid, matrix_name):
        m = hashlib.md5()
                    
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
    