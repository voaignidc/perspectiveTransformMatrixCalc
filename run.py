#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import webbrowser

from app import createApp  

if getattr(sys, 'frozen', False):
    rootPath = os.path.dirname(sys.executable)
elif __file__:
    rootPath = os.path.dirname(__file__)
    
class Config():
    SECRET_KEY = 'hard to guess string'
    ROOT_PATH = rootPath

    @staticmethod
    def init_app(app):
        pass

        
config = Config()
app = createApp(config)

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/")
    app.debug = True
    app.run()  