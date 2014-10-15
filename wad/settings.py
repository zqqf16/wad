#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''App settings'''

import os

from tornado.options import define, options
from tornado.options import parse_config_file, parse_command_line

# Read only settings
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

define('port', default=8000, help='web server running port', type=int)
define('host', default='127.0.0.1:8000',
       help='host address, for download manifest and archives')
define('archive_path', default='archives', help='archive path')
define('config', default='settings.conf', help='configure file path')


def init():
    '''Parse configuration'''

    # parse command line
    parse_command_line()

    if os.path.isfile(options.config):
        parse_config_file(options.config)

    # update archive path
    if not os.path.isabs(options.archive_path):
        options.archive_path = os.path.join(
            options.root_path, options.archive_path)

init()
