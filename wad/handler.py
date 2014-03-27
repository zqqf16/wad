#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.web
from tornado.options import options
from io import BytesIO

import utils
from model import Archive

class FakeBuild(object):
    def __init__(self):
        self.manifest = 'http://fake.plist'
        self.name = 'Fake'

class SingleFileHandler(tornado.web.StaticFileHandler):
    def initialize(self, filename):
        super(SingleFileHandler, self).initialize(options.root)
        self.filename = filename

    def get(self):
        super(SingleFileHandler, self).get(self.filename)

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        archives = Archive.select().order_by(Archive.date.desc())
        self.render('admin.html', archives=archives)

    def post(self):
        file_list = self.request.files.get('ipa_file', [])
        if not file_list:
            self.redirect('/admin')

        content = file_list[0]['body']

        try:
            self.parse_info(content)
        except:
            self.write('Error!')
            return

        self.save_archive(content)
        self.generate_manifest()
        self.generate_index()

        self.redirect('/admin')

    def parse_info(self, content):
        '''Parse infomations from ipa file content'''

        info = utils.get_info(BytesIO(content))

        info['file_name'] = '{name}_{version}_{build}.ipa'.format(**info)
        info['archive_url'] = 'archives/' + info['file_name']
        info['title'] = info['name']
        info['subtitle'] = '{name} {version}'.format(name=info['name'], version=info['version'])
        
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

        html = self.render_string('index.html', host=options.host, title=title, description=description)
        with open(index_path, 'w') as f:
            print 'write'
            f.write(html)
