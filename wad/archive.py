#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import zipfile 
import biplist

from settings import options

class Archive(object):

    # attributes get form plist
    _base_attrs = {
        'version':    'CFBundleShortVersionString',
        'build':      'CFBundleVersion',
        'identifier': 'CFBundleIdentifier',
        'name':       'CFBundleDisplayName',
    }

    _external_attrs = {
        'file_name': '{name}_{version}_{build}.ipa',
        'url': '{options.host}/archives/{name}_{version}_{build}.ipa',
        'title': '{name}',
        'subtitle': '{name} {version}',
    }

    _info_plist_re = re.compile(r'Payload/.*\.app/Info.plist')

    def __init__(self, path, **attrs):
        '''Init archive from file path'''

        self._path = path
        self._parse_attribute(**attrs)

    def _parse_attribute(self, **attrs):
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

        self._base_attrs.update(attrs)
        plist = biplist.readPlistFromString(zip_file.read(info_plist))

        encode = lambda x: x.encode('utf-8') if x else ''
        base = {k: encode(plist.get(v)) for k, v in self._base_attrs.items()}
        external = {k: v.format(options=options, **base) for k, v in self._external_attrs.items()}

        self.__dict__.update(base, **external)

    def __getattr__(self, name):
        return self._attrs.get(name, None)

    def generate_index(self):
        pass

    def generate_manifest(self):
        pass
