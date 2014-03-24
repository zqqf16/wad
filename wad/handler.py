#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from datetime import datetime
import json

class FakeBuild(object):
    def __init__(self):
        self.manifest = 'http://fake.plist'
        self.name = 'Fake'

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        build = FakeBuild()
        self.render('index.html', build=build)

    def post(self):
        self.write('post')

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('get')

    def post(self):
        self.write('post')

class BuildHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('get')

    def post(self):
        self.write('post')
