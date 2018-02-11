#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

def getExtName(path):
    return os.path.splitext(path)[1]

def findImgFiles(path):
    list = os.listdir(path)
    return list

def deleteImgFiles(path):
    os.remove(path)
