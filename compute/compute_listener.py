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

operations = ['add', 'inverse', 'lu', 'transpose', 'multiply', 'list', 'create']

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
    
    # Attempting a valid operation?
    if operation in operations:
        
        # If so, get the actual method for the operation from
        # the Computer
        opfunc = getattr(cc, operation)
        
        msg = opfunc(operands)
    
    socket.send_string(str(msg))


def read_matrix():
    
    return
    
