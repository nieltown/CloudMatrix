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
		file = request.files['csv']
		print "/upload POST"
		path = None
			
		if len(file.filename) < 1:
			print "WHOA"
			title = 'No file uploaded'
		else:
			path = './' + file.filename
			file.save(path)
			title = 'Successful upload'
		return render_template('thanks.html', title=title, filename = file.filename, path = path)
	else:
		print "/upload GET"
		return render_template('upload.html', title='Upload CSV',form=form)


# Returns the inverse of a specified matrix 
# (specified by name in user's scope)
@app.route('/inverse', methods = ['GET'])
def inverse():
	return 'blech'

@app.route('/add', methods = ['GET'])
def add():
	A = request.args.get('A','')
	B = request.args.get('B','')
	
	port = "80"
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
 	
	compute_node = zk.get_compute_node()
 
	socket.connect("tcp://%s:%s" % (compute_node, port))
 	
 	print "Sending..."
	socket.send_string('add %s %s %s' % (get_my_ip(), A, B))

 	print "Sent!"
 	
 	print "Receiving..."
	msg = socket.recv()
	print "Received!"

 	
	return msg

@app.route('/getmatrix', methods = ['GET'])
def getmatrix():
	
	name = request.args.get('name','')
	
	key = ru.get_matrix_hash(get_my_ip(), name)
	
	value = ru.r.get(key)
	
	dict = ast.literal_eval(value)
	
	name = dict['name']
	m = dict['m']
	n = dict['n']
	data = dict['data']
	datamd5 = dict['datamd5']
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	return str(value)
	
	


@app.route('/data', methods = ['GET'])
def get_data():
	m = hashlib.md5()
 	
 	ip = get_my_ip()
 	
 	print ip
 	
	m.update(ip + 'A')
 	
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

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():
	
	sample_matrix_list = [{'name':'a','m':3,'n':3},{'name':'poop','m':32,'n':32}]
	
	keys = ru.r.keys()
	
	matrix_list = []

	for key in keys:
		value = ru.r.get(key)
		print "value: %s" % value
		
		# Only try to create a dict out of it if it can
		# (skip over errors like badly-formed dicts-as-strings
		try:
			value_as_dict = ast.literal_eval(value)
			matrix_list.append(value_as_dict)
		except:
			pass
	
	
	return render_template('index.html', title='cloudmatrix', matrix_list=matrix_list, user=get_my_ip())
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

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return request.remote_addr

zk = zk_util.zk_util('/home/ubuntu/.zk_hosts')

print "getting endpoint"
redis_endpoint = zk.get_redis_primary()
	
print "Endpoint: %s" % redis_endpoint

print "creating redis_util"
ru = redis_util.redis_util(redis_endpoint)

