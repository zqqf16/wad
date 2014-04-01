#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

import settings

from archive import Archive
from settings import options
from generator import index_generator, manifest_generator

def command_line():
    settings.init()

    path = sys.argv[1]

    if not os.path.isfile(path):
        print('Cannot open {}'.format(path))
        return

    archive = Archive(path)

    print('Generate index.html')
    index_generator.generate(archive)

    print('Generate manifest.plist')
    manifest_generator.generate(archive)

    print('Copy file')
    shutil.copyfile(path, os.path.join(options.archive_path, archive.file_name))

    print('Name: {name}\nVersion: {version}\nBuild: {build}'\
          .format(name=archive.name, version=archive.version, build=archive.build))


if __name__ == '__main__':
    command_line()
