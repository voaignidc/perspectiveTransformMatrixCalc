#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint
main = Blueprint('main', __name__)
# 定义main blueprint对象，便于在views.py文件中应用，替代Flask对象
from . import views
