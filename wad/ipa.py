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
 
_manifest_template = '''\
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
   <key>items</key>
   <array>
       <dict>
           <key>assets</key>
           <array>
                <dict>
                   <key>kind</key>
                   <string>software-package</string>
                   <key>url</key>
                   <string>{url}</string>
                </dict>
                {display_image}
                {full_size_image}
           </array>
           <key>metadata</key>
           <dict>
               <key>bundle-identifier</key>
               <string>{identifier}</string>
               <key>bundle-version</key>
               <string>{version}</string>
               <key>kind</key>
               <string>software</string>
               <key>subtitle</key>
               <string>{subtitle}</string>
               <key>title</key>
               <string>{title}</string>
           </dict>
       </dict>
   </array>
</dict>
</plist>
'''
_display_image_template = '''\
                <dict>
                   <key>kind</key>
                   <string>display-image</string>
                   <key>needs-shine</key>
                   <true/>
                   <key>url</key>
                   <string>{url}</string>
                </dict>
                '''
_full_size_image_template = '''\
                <dict>
                   <key>kind</key>
                   <string>full-size-image</string>
                   <key>needs-shine</key>
                   <true/>
                   <key>url</key>
                   <string>{url}</string>
                </dict>
                '''

def manifest(url, identifier, version, title, 
             subtitle='', display_image_url='', 
             full_size_image_url=''):
    '''Create manifest with given informations.

    @param url: ipa package url
    @param identifier: app identifier
    @param version: app version
    @param title: title to display
    @param subtitle: subtitle to display
    @param display_image_url: display image url
    @param full_size_image_url: full size image url

    @return mainfest in XML format
    '''
    
    if display_image_url:
        display_image = _display_image_template.format(url=display_image_url)
    else:
        display_image = ''

    if full_size_image_url:
        full_size_image = _full_size_image_template.format(url=full_size_image_url)
    else:
        full_size_image = ''

    if not subtitle:
        subtitle = title

    return _manifest_template.format(url=url, title=title, version=version, 
                                     subtitle=subtitle, display_image=display_image, 
                                     dentifier=identifier, full_size_image=full_size_image)
