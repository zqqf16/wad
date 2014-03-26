#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.web
from io import BytesIO

import ipa
import settings
from model import Archive

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
        archives = Archive.select().order_by(Archive.date.desc())
        self.render('admin.html', archives=archives)

    def post(self):
        file_list = self.request.files.get('ipa_file', [])
        if not file_list:
            self.redirect('/admin')

        self.archive_operation(file_list[0]['body'])
        self.redirect('/admin')

    def archive_operation(self, content):
        try:
            info = ipa.get_info(BytesIO(content))
        except:
            return

        file_name = "{name}_{version}_{build}.ipa".format(**info)
        size = len(content)
        archive = Archive.create(file_name=file_name, size=size, **info)
        archive.save()

        path = os.path.join(settings.archive_dir, file_name)
        with open(path, 'wb') as f:
            f.write(content)

class BuildHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('get')

    def post(self):
        self.write('post')
