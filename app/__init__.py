#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

def createApp(config):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['UPLOADED_PHOTOS_DEST'] = config.ROOT_PATH + '/app/static/images' # 图像上传到的路径
    
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch_request_class(app) 
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
