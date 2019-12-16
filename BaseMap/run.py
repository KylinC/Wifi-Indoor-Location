#!/usr/bin/env python
#encoding=utf-8

import sys
from flask import Flask, render_template, request, url_for, Response
import json
# from neo4j import GraphDatabase

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('basic.html')

if __name__ == "__main__":
    app.run(debug = True)