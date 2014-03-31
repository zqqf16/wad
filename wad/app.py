#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver

from tornado.options import define, options

from handler import *

define('port', default=8000, help='running port', type=int)
define('archives', default='archives', help='archives path')
define('root', default='../example', help='root directory')
define('host', default='192.168.0.2:8000', help='host address')

class App(tornado.web.Application):
    def __init__(self):
        archives_path = os.path.join(options.root, options.archives)

        handlers = [
            (r'[/]?', SingleFileHandler, {'filename': 'index.html'}),
            (r'/manifest.plist', SingleFileHandler, {'filename': 'manifest.plist'}),

            (r'/admin[/]?', AdminHandler),
            (r'/archives/(.*)', tornado.web.StaticFileHandler, {'path': archives_path}),
        ]

        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        }

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    
    #Load config
    tornado.options.parse_command_line()

    if not options.host.startswith('http'):
        print options.host
        options.host = 'http://' + options.host

    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
