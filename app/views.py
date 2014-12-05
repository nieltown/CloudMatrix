from flask import render_template
from flask import request
from app import app
import os
import zmq
import requests

import zk_util
from forms import UploadForm

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadForm()
	
	if request.method == 'POST':
		file = request.files['myFile']
		print file
		file.save('../' + file.filename)
		return render_template('thanks.html', title='Successful upload', filename = file.filename)
	else:
		return render_template('upload.html', title='Upload CSV',form=form)

@app.route('/data', methods = ['GET'])
def get_data():
	return "i got your data right here, pal"

@app.route('/')
@app.route('/index')
def index():
	
	print "blah blah blah"
	
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

host_string = init_zk_hosts()
zk = zk_util.zk_util(host_string)

