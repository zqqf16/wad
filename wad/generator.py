#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from tornado import template

from archive import Archive
from settings import options, template_path

class Generator(object):
    
    def __init__(self, file_name, template_name, **attrs):
        self.template_name = template_name
        self.attrs = attrs
        self.file_name=file_name

    @property
    def template(self):
        loader = template.Loader(template_path)
        return loader.load(self.template_name)

    def generate(self, archive):
        html = self.template.generate(archive=archive, options=options, **self.attrs)
        dest = os.path.join(options.root_path, self.file_name)
        with open(dest, 'w') as f:
            f.write(html)

index_generator = Generator('index.html', 'index.html', manifest_url=options.host+'/manifest.plist')
manifest_generator = Generator('manifest.plist', 'manifest.plist')
