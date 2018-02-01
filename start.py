#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import webbrowser

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

if getattr(sys, 'frozen', False):
    rootPath = os.path.dirname(sys.executable)
elif __file__:
    rootPath = os.path.dirname(__file__)    

app = Flask(__name__)
app.config['SECRET_KEY'] = 'noPasswordIsOk'
app.config['UPLOADED_PHOTOS_DEST'] = rootPath + '/images' # 文件上传到的路径

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 

class UploadForm(FlaskForm):
    """上传图像文件的表单"""
    photo = FileField(validators=[
        FileAllowed(photos, u'只能上传图片！'), 
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')    
    
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        fileUrl = photos.url(filename)
    else:
        fileUrl = None
    return render_template('base.html', form=form, fileUrl=repr(fileUrl))

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')
    
if __name__ == '__main__':
    #webbrowser.open(rootPath+"/templates/base.html")
    webbrowser.open("http://127.0.0.1:5000/")
    app.debug = True
    app.run()