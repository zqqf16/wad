#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Web'''

from flask import Flask

from db import init_database

#blueprint
from admin import admin_app


# default settings
_UPLOAD_FOLDER = '/var/tmp/'
_DATABASE_NAME = 'wad.db'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = _UPLOAD_FOLDER
app.config['DATABASE_NAME'] = _DATABASE_NAME

@app.route('/')
def index():
    '''Index'''

    return 'Hello World'

#register blueprint
app.register_blueprint(admin_app, url_prefix='/admin')

#init database
init_database(app.config['DATABASE_NAME'])

if __name__ == '__main__':
    app.run(debug=True)
