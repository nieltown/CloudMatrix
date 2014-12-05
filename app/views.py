from flask import render_template
from flask import request
from flask import jsonify
from app import app
import os
import zmq
import requests
import hashlib
import random
import ast

import redis_util
import zk_util
from forms import UploadForm

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadForm()
	
	if request.method == 'POST':
		file = request.files['myFile']
		print "/upload POST"
		file.save('../' + file.filename)
		return render_template('thanks.html', title='Successful upload', filename = file.filename)
	else:
		print "/upload GET"
		return render_template('upload.html', title='Upload CSV',form=form)


# Returns the inverse of a specified matrix 
# (specified by name in user's scope)
@app.route('/inverse', methods = ['GET'])
def inverse():
	return 'blech'

@app.route('/data', methods = ['GET'])
def get_data():
	m = hashlib.md5()
 	
 	ip = get_my_ip()
 	
 	print ip
 	
	m.update("%spoop" % ip)
 	
	key = m.digest()
 	
 	if ru.r.get(key):
 		return "key %s is present!" % key
 	
	value = {"name":"blah","m":35,"n":36}
 	
	print "key: %s" % key
 	
	ru.r.set(key, value)
# 	
# 	print "value: %s" % ru.r.get(key)
	
	print "getting keys"
	keys = ru.r.keys()

	response = ""	
	for key in keys:
# 		ru.r.delete(key)
		print "key: %s" % key
		print "\t%s" % ru.r.get(key)

	return str(response)

@app.route('/')
@app.route('/index')
def index():
	
	sample_matrix_list = [{'name':'a','m':3,'n':3},{'name':'poop','m':32,'n':32}]
	
	keys = ru.r.keys()
	
	matrix_list = []
	
	for key in keys:
		value = ru.r.get(key)
		print "value: %s" % value
		
		matrix_list.append(value)
		
	return render_template('index.html', matrix_list=keys, user={'nickname':'Nieltown'})
# 	port = "80"
# 	context = zmq.Context()
# 	socket = context.socket(zmq.REQ)
# 	
# 	compute_node = zk.get_compute_node()
# 
# 	socket.connect("tcp://%s:%s" % (compute_node, port))
# 	
# 	csv = open('/home/ubuntu/cloudmatrix/data/inverse_01.csv','r')
# 
# 	data = csv.read()
# 
# 	socket.send(data)
# 
# 	msg = socket.recv()
# 	
# 	return msg
	

def init_zk_hosts():
	hosts = []
	
	z = open('/home/ubuntu/.zk_hosts')
	
	for line in z.readlines():
		
		hosts.append(line.replace('\r\n',''))
	
	host_string = ','.join(hosts)
	
	return host_string

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return request.remote_addr

def get_matrix_hash(matrix_name):
	m = hashlib.md5()
	ip = get_my_ip()
				
	m.update("%s%s" % (ip, matrix_name))
	
	return m.digest()

host_string = init_zk_hosts()
zk = zk_util.zk_util(host_string)

print "getting endpoint"
redis_endpoint = zk.get_redis_primary()
	
print "Endpoint: %s" % redis_endpoint

print "creating redis_util"
ru = redis_util.redis_util(redis_endpoint)

