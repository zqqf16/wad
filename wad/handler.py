#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.web

from io import BytesIO

from archive import Archive
from settings import options
from generator import index_generator, manifest_generator

class SingleFileHandler(tornado.web.StaticFileHandler):
    def initialize(self, filename):
        super(SingleFileHandler, self).initialize(options.root_path)
        self.filename = filename

    def get(self):
        super(SingleFileHandler, self).get(self.filename)

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin.html')

    def post(self):
        file_list = self.request.files.get('ipa_file', [])
        if not file_list:
            self.redirect('/admin')

        content = file_list[0]['body']

        archive = Archive(BytesIO(content))
        try:
            archive = Archive(BytesIO(content))
        except:
            self.write('Error!')
            return

        index_generator.generate(archive)
        manifest_generator.generate(archive)

        with open(options.archive_path+archive.file_name, 'wb') as f:
            f.write(content)

        self.redirect('/admin')
