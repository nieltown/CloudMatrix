import zmq
import time
import requests 
import simplejson as json
import redis

port = "80"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

while True:
    msg = socket.recv()
    
    print msg
    
    redisEndpoint = ''
    redisPort = 6379
    
    r = redis.StrictRedis(host=redisEndpoint, port=redisPort)
    
    val = str(r.keys())
    
    socket.send(msg)

