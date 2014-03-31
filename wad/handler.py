#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.web

from tornado.options import options
from io import BytesIO

from archive import Archive

class SingleFileHandler(tornado.web.StaticFileHandler):
    def initialize(self, filename):
        super(SingleFileHandler, self).initialize(options.root)
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

        try:
            self.archive = Archive(BytesIO(content))
        except:
            self.write('Error!')
            return

        self.parse_info()
        self.save_archive(content)
        self.generate_manifest()
        self.generate_index()

        self.redirect('/admin')

    def parse_info(self):
        info = self.archive.attributes

        info['file_name'] = '{name}_{version}_{build}.ipa'.format(**info)
        info['archive_url'] = '{}/archives/{}'.format(options.host, info['file_name'])
        info['title'] = info['name']
        info['subtitle'] = '{} {}'.format(info['name'], info['version'])
        
        self.info = info

    def save_archive(self, content):
        path = os.path.join(options.root, options.archives, self.info['file_name'])

        with open(path, 'wb') as f:
            f.write(content)

    def generate_manifest(self):
        html = self.render_string('manifest.plist', **self.info)
        path = os.path.join(options.root, 'manifest.plist')

        with open(path, 'w') as f:
            f.write(html)

    def generate_index(self):
        index_path = os.path.join(options.root, 'index.html')
        title = self.info['name']
        description = '{} {}'.format(self.info['version'], self.info['build'])
        manifest_url = '{}/manifest.plist'.format(options.host)

        html = self.render_string('index.html', manifest_url=manifest_url, title=title, description=description)
        with open(index_path, 'w') as f:
            f.write(html)
