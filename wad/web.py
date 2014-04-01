#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver

import settings

from settings import options, template_path, static_path
from handler import *

class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'[/]?', SingleFileHandler, {'filename': 'index.html'}),
            (r'/manifest.plist', SingleFileHandler, {'filename': 'manifest.plist'}),

            (r'/admin[/]?', AdminHandler),
            (r'/archives/(.*)', tornado.web.StaticFileHandler, {'path': options.archive_path}),
        ]

        settings = {
            'template_path': template_path,
            'static_path': static_path,
        }

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
