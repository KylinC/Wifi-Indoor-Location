#!/usr/bin/env python
#encoding=utf-8

# www.kylinchen.top

import psutil  # system resource
import time

from threading import Lock

import sys
from flask import Flask, render_template, request, url_for, Response
from flask_socketio import SocketIO, emit
import json

from coordination import coord
from scanner import Scanner
from data import Dataset
import torch
import os

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()

with torch.no_grad():
    rnn = torch.load("result/rnn.pkl")
scanner = Scanner()
dataset = Dataset()
seqLen = 5

def prediction(feature):
    with torch.no_grad():
        os.system("networksetup -setairportpower en0 on")
        result = scanner.scan_all()
        # print(result)
        newFeature = dataset.result2feature(result).view(1,1,-1)
        feature = torch.cat([feature, newFeature], dim=0)

        if feature.shape[0]>seqLen:
            feature = feature[1:6]
        if feature.shape[0]<seqLen:
            return feature,"213"

        hidden = rnn.initHidden()
        for i in range(feature.shape[0]):
            input = feature[i]
            output, hidden = rnn(input, hidden)

        pos = dataset.output2pos(output)
        os.system("networksetup -setairportpower en0 off")
        # print(pos)
        return feature,pos

def background_thread():
    feature = torch.randn([0])
    data = []
    count = 0
    data_before = [{}]
    while True:
        socketio.sleep(1)
        count += 1
        t = time.strftime('%M:%S', time.localtime()) 
        print("time is:"+t)
        # 
        # data online computing
        data = []
        feature,room_num = prediction(feature)
        print("the prediction position is: "+room_num)
        try:
            data.append(coord[room_num])
        except:
            data.append(coord['206'])

        # print(data)
        # 
        # cpus = psutil.cpu_percent(interval=None, percpu=True) 
        if(data_before != data):
            socketio.emit('server_response',
                      {'data': data},
                      namespace='/test') # default broadcast = True
            data_before = data
            print("data update from socket!")
        # print("push it!")

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('basic.html',async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

if __name__ == "__main__":
    socketio.run(app, debug=True)
    # app.run(debug = True)