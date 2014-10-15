#!/usr/bin/env python

'''Plist operation'''

from __future__ import unicode_literals

import re
import zipfile
import biplist

def get_plist_from_ipa(path):
    '''Get plist file from IPA

    @param path: IPA file path
    @return plist bytes
    '''

    plist_file_re = re.compile(r'Payload/.*\.app/Info.plist')

    try:
        ipa = zipfile.ZipFile(path)
    except:
        raise IOError('Failed to read IPA file')

    file_list = ipa.namelist()

    plist_path = ""
    for file_name in file_list:
        if plist_file_re.match(file_name):
            plist_path = file_name
            break

    else:
        raise NameError('Info.plist not found in this IPA')

    try:
        plist = ipa.read(plist_path)
    except:
        raise IOError('Fail to read plist')

    return plist

def get_info(path):
    '''Get plist file from IPA

    @param path: IPA file path
    @return {'version': '', 'build': '', 'identifier': '', 'name':''}
    '''

    base_attrs = {
        'version':    b'CFBundleShortVersionString',
        'build':      b'CFBundleVersion',
        'identifier': b'CFBundleIdentifier',
        'name':       b'CFBundleDisplayName',
    }

    try:
        plist = biplist.readPlistFromString(get_plist_from_ipa(path))
    except:
        raise IOError('Fail to read plist')

    return {k: plist.get(v).decode() for k, v in base_attrs.items()} #pylint: disable=E1103
