#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import webbrowser

if getattr(sys, 'frozen', False):
    rootPath = os.path.dirname(sys.executable)
elif __file__:
    rootPath = os.path.dirname(__file__)    
    
webbrowser.open(rootPath+"/templates/base.html")