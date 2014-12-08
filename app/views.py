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
@app.route('/invert', methods = ['GET'])
def invert():
	A = request.args.get('A','')
	store = request.args.get('store','')
	
	socket = get_socket()
	
	msg = 'invert %s %s %s' % (get_my_ip(), A, store)
	print "Sending... %s" % msg
	socket.send_string(msg)
	print "Sent!"
	print "Receiving..."
	msg = socket.recv()
	socket.close()
	
	return msg

@app.route('/add', methods = ['GET'])
def add():
	A = request.args.get('A','')
	B = request.args.get('B','')
	store = request.args.get('store','')
	
	print "store = %s" % store
	
	socket = get_socket()
 	
 	print "Sending..."
	socket.send_string('add %s %s %s %s' % (get_my_ip(), A, B, store))

 	print "Sent!"
 	
 	print "Receiving..."
 	
	msg = socket.recv()
	socket.close()
 	
	return msg

@app.route('/multiply', methods = ['GET'])
def multiply():
	A = request.args.get('A','')
	B = request.args.get('B','')
	store = request.args.get('store','')
	
	socket = get_socket()
 	
 	print "Sending..."
	socket.send_string('multiply %s %s %s %s' % (get_my_ip(), A, B, store))

 	print "Sent!"
 	
 	print "Receiving..."
 	
	msg = socket.recv()
	socket.close()
 	
	return msg



@app.route('/getmatrix', methods = ['GET'])
def getmatrix():
	
	name = request.args.get('name','')
	
# 	key = du.get_matrix_hash(get_my_ip(), name)

	socket = get_socket()
	
	socket.send_string("getmatrix %s %s" % (get_my_ip(), name))
	
	val = socket.recv()	
	
	return val
	

# Returns a list of all the data in Redis owned by the user
@app.route('/list', methods = ['GET'])
def list():
	
	socket = get_socket()
 	
 	socket.send_string("list %s" % get_my_ip())

	msg = socket.recv()

	socket.close()

	print msg


	return str(msg)

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

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return request.remote_addr

@app.route("/doobies", methods=["GET"])
def doobies():
	socket = get_socket()
	socket.send_string("doobies blah blah")
	
	msg = socket.recv()
	
	return msg

@app.route("/create", methods=["GET"])
def create():
	
	name = request.args.get('name')
	data = request.args.get('data')
	datamd5 = get_md5(data)
	userid = get_my_ip()
	
	socket = get_socket()
	
	socket.send_string('create %s %s %s' % (userid, name, data))
	msg = socket.recv()
	
	socket.close()
	
	return msg

@app.route("/populate", methods=["GET"])
def populate():
	
	socket = get_socket()
	
	socket.send_string('populate %s' % get_my_ip())
	
	msg = socket.recv()
	
	socket.close()
	
	return msg
	

def get_socket():
	
	compute_node = zk.get_compute_node()
 
 	port = "80"
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
 
	socket.connect("tcp://%s:%s" % (compute_node, port))
	
	return socket

def get_md5(data):
        
    m = hashlib.md5()
    
    m.update("%s" % data)
    
    return m.digest()
   

zk = zk_util.zk_util('/home/ubuntu/.zk_hosts')

print "getting endpoint"
redis_endpoint = zk.get_redis_primary()

	
print "Endpoint: %s" % redis_endpoint

print "creating redis_util"
ru = redis_util.redis_util(redis_endpoint)

