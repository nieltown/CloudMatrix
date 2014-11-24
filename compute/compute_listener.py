import zmq
import time
import requests 
import simplejson as json
import redis
import numpy

port = "80"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

rowlist = []

while True:
    msg = socket.recv()

    for line in msg.split('\n'):
        
        if line:
            # Have to 
            #    1. Parse elements from each row
            #    2. Remove the semicolon at the end of the line
            #    3. Convert the elements to floats
            row = map(float,line.replace(';','').split(','))
            rowlist.append(row)
    
    print rowlist
    
    arr = numpy.vstack(rowlist)
    
    print arr.shape
    
    inv = numpy.linalg.inv(arr)
     
    print "---"
     
    print inv
    
#     redisEndpoint = ''
#     redisPort = 6379
#     
#     r = redis.StrictRedis(host=redisEndpoint, port=redisPort)
#     
#     val = str(r.keys())
    
    socket.send(msg)

