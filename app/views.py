from flask import render_template
from flask import request
from app import app

import os
import zmq

import requests

@app.route('/')
@app.route('/index')
def index():
	
	port = "80"
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://54.173.133.81:%s" % port)
	
	csv = open('/home/ubuntu/cloudmatrix/data/inverse_01.csv','r')
	
	data = csv.read()

	socket.send(data)
	
	msg = socket.recv()
	
	return msg
	
	


