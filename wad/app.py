#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import tornado.ioloop
import tornado.web
import tornado.httpserver

from handler import *

class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/admin[/]?', AdminHandler),
            (r'/build/(.*)', BuildHandler),
        ]

        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
        }

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

