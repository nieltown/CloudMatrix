from flask import render_template
from flask import request
from flask import jsonify
from app import app
import os
import zmq
import requests

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

@app.route('/data', methods = ['GET'])
def get_data():
	
	print "getting endpoint"
	redis_endpoint = zk.get_redis_endpoint()
	
	print "creating redis_util"
	ru = redis_util.redis_util(redis_endpoint)
	
	print "getting keys"
	keys = ru.r.keys(request.remote_addr)
	
	if len(keys) == 0:
		print "FUCK"
	
	return str(keys)
	
	
	
	
	

@app.route('/')
@app.route('/index')
def index():
	
	port = "80"
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	
	compute_node = zk.get_compute_node()

	socket.connect("tcp://%s:%s" % (compute_node, port))
	
	csv = open('/home/ubuntu/cloudmatrix/data/inverse_01.csv','r')

	data = csv.read()

	socket.send(data)

	msg = socket.recv()
	
	return msg
	
	
def init_zk_hosts():
	hosts = []
	
	z = open('/home/ubuntu/.zk_hosts')
	
	for line in z.readlines():
		
		hosts.append(line.replace('\r\n',''))
	
	host_string = ','.join(hosts)
	
	return host_string

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

host_string = init_zk_hosts()
zk = zk_util.zk_util(host_string)

