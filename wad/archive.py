#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import zipfile 
import biplist

class Archive(object):

    # default attributes
    default_attributes = {
        'version':    'CFBundleShortVersionString',
        'build':      'CFBundleVersion',
        'identifier': 'CFBundleIdentifier',
        'name':       'CFBundleDisplayName',
    }

    _info_plist_re = re.compile(r'Payload/.*\.app/Info.plist')

    def __init__(self, path, **attrs):
        '''Init archive from file path'''

        self._path = path
        self.parse_attribute(**attrs)

    def parse_attribute(self, **attrs):
        '''Get ipa informations

        @param attrs: the attributes name
        @return: info dictionary
        '''

        zip_file = zipfile.ZipFile(self._path)
        namelist = zip_file.namelist()

        info_plist = None
        for f in namelist:
            if self._info_plist_re.match(f):
                info_plist = f
                break
        else:
            raise NameError('Info.plist not found')

        self.default_attributes.update(attrs)
        plist = biplist.readPlistFromString(zip_file.read(info_plist))

        self.attributes = {k: plist.get(v).encode('utf-8') for k, v in self.default_attributes.items()}
