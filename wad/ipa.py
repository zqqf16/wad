#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import zipfile 
import biplist

# all available attributes
attributes = {
    'version':    'CFBundleShortVersionString',
    'build':      'CFBundleVersion',
    'identifier': 'CFBundleIdentifier',
    'name':       'CFBundleDisplayName',
}

class IPA(object):
    '''A wrapper of ipa package'''

    info_plist_re = re.compile(r'Payload/.*\.app/Info.plist')

    def __init__(self, path):
        zip_file = zipfile.ZipFile(path)
        all_files = zip_file.namelist()

        info = None
        for f in all_files:
            if self.info_plist_re.match(f):
                info = f
                break

        if not info:
            raise NameError('Info.plist not found')

        self.info = biplist.readPlistFromString(zip_file.read(info))

        for attr, name in attributes.items():
            setattr(self, attr, self.get_attribute(name))
    
    def get_attribute(self, attr):
        '''Get attribute from Info.plist
        
        @param attr: attribute name, e.g. "CFBundleIdentifier"
        '''
        return self.info.get(attr).encode('utf-8')

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
