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

operations = ['add', 'invert', 'lu', 'transpose', 'multiply', 'list', \
              'create', 'getmatrix', 'populate']

while True:
    print "..."
    msg = socket.recv()
    print "Received data."

    tokens = msg.split()
    
    operation = tokens[0]
    ip = tokens[1]
    operands = tokens[2:len(tokens)]
    
    cc = cloudmatrix_compute.Computer(ip)
    
    print "Requested operation: %s" % operation
    
    # Attempting a valid operation?
    if operation in operations:
        
        # If so, get the actual method for the operation from
        # the Computer
        opfunc = getattr(cc, operation)
        
        if len(operands) > 0:
            print "At least onezo"
            msg = opfunc(operands)
        else:
            print "Nonezo"
            msg = opfunc()
    else:
        msg = "Invalid operation: %s!" % operation
        
    socket.send_string(str(msg))


def read_matrix():
    
    return
    
