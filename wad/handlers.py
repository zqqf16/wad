#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''URL handlers'''

import tornado.web
from tornado.options import options

import os
from io import BytesIO

import model
import plist


def get_manifest_url(identifier):
    '''Get manifest url'''
    url_format = 'https://{}/manifest/{}.plist'
    return url_format.format(options.host, identifier)


def get_ipa_url(identifier):
    '''Get ipa file url'''
    url_format = 'https://{}/archive/{}.ipa'
    return url_format.format(options.host, identifier)


def get_ipa_path(identifier):
    '''Get ipa file path'''
    return os.path.join(options.archive_path,
                        identifier + '.ipa')


class SingleFileHandler(tornado.web.StaticFileHandler):

    def initialize(self, filename):
        super(SingleFileHandler, self).initialize(options.root_path)
        self.filename = filename

    def get(self):
        super(SingleFileHandler, self).get(self.filename)


class IndexHandler(tornado.web.RequestHandler):  # pylint: disable=R0904

    '''Index handler'''

    def get(self):
        archives = model.Archive.all().values()
        self.render('index.html', url=get_manifest_url, archives=archives)


class ManifestHandler(tornado.web.RequestHandler):

    '''Manifest handler'''

    def get(self, identifier):  # pylint: disable=W0221
        if not identifier:
            self.write('Identifier cannot be empty')
            return

        archive = model.Archive.get(identifier)
        if not archive:
            self.write('Identifier:[{}] not found'.format(identifier))
            return

        self.render('manifest.plist', url=get_ipa_url, archive=archive)


class AdminHandler(tornado.web.RequestHandler):  # pylint: disable=R0904

    '''Admin handler'''

    def get(self):
        archives = model.Archive.all().values()
        self.render('admin.html', archives=archives)


class DeleteHandler(tornado.web.RequestHandler):  # pylint: disable=R0904

    '''Delete handler'''

    def get(self):
        identifier = self.get_argument('id', None)
        if not identifier:
            self.write('Identifier cannot be empty')
            return

        if identifier.startswith('.'):
            self.write('Identifier:[{}] is illegal'.format(identifier))
            return

        model.Archive.delete(identifier)

        try:
            os.remove(get_ipa_path(identifier))
        except OSError:
            pass

        self.redirect('/admin')

class UploadHandler(tornado.web.RequestHandler):  # pylint: disable=R0904

    '''IPA upload handler'''

    def get(self):
        self.redirect('/admin')

    def post(self):
        file_list = self.request.files.get('ipa_file', None)
        if not file_list:
            self.redirect('/admin')

        content = file_list[0]['body']

        try:
            ipa_info = plist.get_info(BytesIO(content))
        except IOError:
            self.write('Error: failed to parse IPA file')
            return

        archive = model.Archive(**ipa_info)  # pylint: disable=W0612

        model.Archive.add(archive)
        model.Archive.save()

        dest_path = get_ipa_path(archive.identifier)
        with open(dest_path, 'wb') as ipa_file:
            ipa_file.write(content)

        self.redirect('/admin')
