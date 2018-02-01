#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import webbrowser


from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


if getattr(sys, 'frozen', False):
    rootPath = os.path.dirname(sys.executable)
elif __file__:
    rootPath = os.path.dirname(__file__)    

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard_to_guess_string'




class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    # name = None
    # form = NameForm()
    # if form.validate_on_submit():
        # name = form.name.data
        # form.name.data = ''
    return render_template('base.html')#, form=form, name=name)
    
    
if __name__ == '__main__':
    #webbrowser.open(rootPath+"/templates/base.html")
    webbrowser.open("http://127.0.0.1:5000/")
    app.debug = True
    app.run()