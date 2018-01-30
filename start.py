#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import webbrowser
from flask import Flask

if getattr(sys, 'frozen', False):
    rootPath = os.path.dirname(sys.executable)
elif __file__:
    rootPath = os.path.dirname(__file__)    

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('base.html')
    
if __name__ == '__main__':
    #webbrowser.open(rootPath+"/templates/base.html")
    webbrowser.open("http://127.0.0.1:5000/")
    app.debug = True
    app.run()