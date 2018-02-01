#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from . import main
photos = UploadSet('photos', IMAGES)

class UploadForm(FlaskForm):
    """上传图像文件的表单"""
    photo = FileField(validators=[
        FileAllowed(photos, u'只能上传图片！'), 
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')    
    
def getSuffixName(fileName):
    pass
      
@main.route('/', methods=['GET', 'POST'])
def base():
    form = UploadForm()
    if form.validate_on_submit():
        fileName = photos.save(form.photo.data)
        #suffixName
        fileUrl = photos.url(fileName)
    else:
        fileUrl = None
    return render_template('base.html', form=form, fileUrl=repr(fileUrl))

@main.route('/tutorial')
def tutorial():
    return render_template('tutorial.html') 