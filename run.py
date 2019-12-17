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

scanner = Scanner()
dataset = Dataset()

def prediction(mlp, lastPos):
    # print("Hello")
    with torch.no_grad():
        os.system("networksetup -setairportpower en0 on")
        result = scanner.scan_all()
        
        feature = dataset.result2feature(result)
        predict = mlp(feature)
        pos = dataset.output2pos(predict)

        if lastPos not in dataset.adj2(pos,dist=2):
            # print(pos) 
            # print(lastPos)
            pos = lastPos
        
        os.system("networksetup -setairportpower en0 off")
        # print(pos)
        return pos

def rnnPrediction(feature, rnn):
    with torch.no_grad():
        os.system("networksetup -setairportpower en0 on")
        result = scanner.scan_all()
        # print(result)
        newFeature = dataset.result2feature(result).view(1,1,-1)
        feature = torch.cat([feature, newFeature], dim=0)

        if feature.shape[0]>seqLen:
            feature = feature[:5]
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
    data = []
    count = 0
    data_before = [{}]
    room_num = 'sm1'
    mlp = torch.load("result/mlp_6.pkl")
    while True:
        socketio.sleep(1)
        count += 1
        t = time.strftime('%M:%S', time.localtime()) 
        # print("time is:"+t)
        # 
        # data online computing
        data = []
        room_num = prediction(mlp, room_num)
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
            # print("data update from socket!")
        # print("push it!")

def background_thread_rnn():
    feature = torch.randn([0])
    data = []
    count = 0
    data_before = [{}]
    rnn = torch.load("result/rnn_random100.pkl")
    while True:
        socketio.sleep(1)
        count += 1
        t = time.strftime('%M:%S', time.localtime()) 
        print("time is:"+t)
        # 
        # data online computing
        data = []
        feature,room_num = rnnPrediction(feature, rnn)
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
    socketio.run(app, debug=True, port=5000)
    # app.run(debug = True)