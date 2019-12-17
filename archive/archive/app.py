# -*- coding:utf-8 -*-

"""
    Front-End developed by Echarts, https://kylinchen.top/Wifi-Indoor-Location/
    Kylinchen, www.kylinchen.top, k1017856853@icloud.com
"""

import psutil    
import time

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

from scanner import Scanner
from config import INIT_AP

from threading import Lock


'''
Set this variable to "threading", "eventlet" or "gevent" to test the
different async modes, or leave it set to None for the application to choose
the best option based on installed packages.
'''
async_mode = "threading"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nilyk'
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()

def background_thread():
    count = 0
    my_scanner = Scanner()
    while True:
        socketio.sleep(1.5)
        count += 1
        t = time.strftime('%M:%S', time.localtime())
        result = my_scanner.scan_aim()
        cpus = []
        for item in INIT_AP:
            cpus.append(result[item]["signal"])
        # print(cpus)
        socketio.emit('server_response',
                      {'data': [t] + list(cpus)[0:4], 'count': count},
                      namespace='/test')
        # print([t] +list(cpus)[0:4])
        # print(100*'*')

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


socketio.run(app, debug=True)