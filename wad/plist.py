#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Plist operation'''

import re
import zipfile
import biplist

def get_info(path):
    '''Get plist file from IPA

    @param path: IPA file path
    @return {'version': '', 'build': '', 'identifier': '', 'name':''}
    '''

    plist_re = re.compile(r'Payload/.*\.app/Info.plist')

    base_attrs = {
        'version':    'CFBundleShortVersionString',
        'build':      'CFBundleVersion',
        'identifier': 'CFBundleIdentifier',
        'name':       'CFBundleDisplayName',
    }

    try:
        ipa = zipfile.ZipFile(path)
    except:
        raise IOError('Fail to open IPA file')

    file_list = ipa.namelist()

    plist_path = None
    for file_name in file_list:
        if plist_re.match(file_name):
            plist_path = file_name
            break
    else:
        raise NameError('Info.plist not found')

    try:
        plist = biplist.readPlistFromString(ipa.read(plist_path))
    except:
        raise IOError('Fail to read plist')

    encode = lambda x: x.encode('utf-8') if x else ''

    return {k: encode(plist.get(v)) for k, v in base_attrs.items()}
