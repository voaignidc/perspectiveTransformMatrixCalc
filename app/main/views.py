#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from . import main
from .fileManage import getExtName

photos = UploadSet('photos', IMAGES)
class UploadForm(FlaskForm):
    """上传图像文件的表单"""
    photo = FileField(validators=[
        FileAllowed(photos, u'只能上传图片！'), 
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')

class DoPerspectForm(FlaskForm):
    name = StringField(u'坐标:')
    submit = SubmitField(u'运行透视变换')

@main.route('/', methods=['GET', 'POST'])
def index():
    uploadForm = UploadForm()
    doPerspectForm = DoPerspectForm()

    return render_template('index.html', uploadForm=uploadForm, doPerspectForm=doPerspectForm)

@main.route('/upload', methods=['POST'])
def upload():
    uploadForm = UploadForm()
    doPerspectForm = DoPerspectForm()

    if uploadForm.validate_on_submit():
        # extName = getExtName(uploadForm.photo.data.filename)
        # uploadForm.photo.data.filename = 'src_userInput' + extName
        fileName = photos.save(uploadForm.photo.data)
        fileUrl = photos.url(fileName)
        session['fileUrl'] = fileUrl
    else:
        fileUrl = None

    return render_template('index.html', uploadForm=uploadForm,
                           doPerspectForm=doPerspectForm, fileUrl=repr(session.get('fileUrl')))


@main.route('/doPerspect', methods=['GET', 'POST'])
def doPerspect():
    uploadForm = UploadForm()
    doPerspectForm = DoPerspectForm()

    if doPerspectForm.validate_on_submit():
        print('run perspect')
        print(doPerspectForm.name)
    return render_template('index.html', uploadForm=uploadForm,
                           doPerspectForm=doPerspectForm, fileUrl=repr(session.get('fileUrl')))

@main.route('/tutorial')
def tutorial():
    return render_template('tutorial.html') 