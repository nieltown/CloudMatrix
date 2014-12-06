import zmq
import time
import requests 
import simplejson as json

import cloudmatrix_compute

port = "80"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

rowlist = []

operations = ['add', 'inverse', 'lu', 'transpose', 'multiply']



while True:
    print "..."
    msg = socket.recv()
    print "Received data."

    tokens = msg.split()
    
    operation = tokens[0]
    ip = tokens[1]
    operands = tokens[2:len(tokens)]
    
    cc = cloudmatrix_compute.Computer(ip)
    
    print tokens
    
    if operation in operations:
        opfunc = getattr(cc, operation)
        
        print opfunc
        
        opfunc(operands)
    
    
    
    socket.send_string("Got it")
#     rowlist = []
# 
#     for line in msg.split('\n'):
#         
#         if line:
#             # Have to 
#             #    1. Parse elements from each row
#             #    2. Remove the semicolon at the end of the line
#             #    3. Convert the elements to floats
#             row = map(float,line.replace(';','').split(','))
#             rowlist.append(row)
#     
#     arr = numpy.vstack(rowlist)
#     
#     print "---"
#     print arr
#     print "---"
#     
#     
#     inv = numpy.linalg.inv(arr)
#     
# #     redisEndpoint = ''
# #     redisPort = 6379
# #     
# #     r = redis.StrictRedis(host=redisEndpoint, port=redisPort)
# #     
# #     val = str(r.keys())
#     
#     socket.send(str(inv))

def read_matrix():
    
    return
    
