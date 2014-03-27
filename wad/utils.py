#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import zipfile 
import biplist

def get_info(path, **attrs):
    '''Get ipa informations

    @param path: ipa file path
    @param attrs: the attributes na
    @return: info dictionary
    '''

    attributes = {
        'version':    'CFBundleShortVersionString',
        'build':      'CFBundleVersion',
        'identifier': 'CFBundleIdentifier',
        'name':       'CFBundleDisplayName',
    }
    info_plist_re = re.compile(r'Payload/.*\.app/Info.plist')

    zip_file = zipfile.ZipFile(path)
    namelist = zip_file.namelist()

    info_plist = None
    for f in namelist:
        if info_plist_re.match(f):
            info_plist = f
            break
    else:
        raise NameError('Info.plist not found')

    attributes.update(attrs)
    plist = biplist.readPlistFromString(zip_file.read(info_plist))

    return {k: plist.get(v).encode('utf-8') for k, v in attributes.items()}
