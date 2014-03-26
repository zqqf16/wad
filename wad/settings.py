#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

archive_dir = './motionpro'

def init():
    '''Do some init jobs'''

    if not os.path.isdir(archive_dir):
        #Create archive directory
        os.mkdir(archive_dir)

init()
