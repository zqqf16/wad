#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Web'''

import tornado.web
import tornado.ioloop

from tornado.options import options

import settings
import handlers


class App(tornado.web.Application):

    '''Web Application'''

    def __init__(self):
        url_handlers = [
            (r'[/]?', handlers.IndexHandler),
            (r'/manifest/(.*).plist', handlers.ManifestHandler),
            (r'/archive/(.*)', tornado.web.StaticFileHandler,
             {'path': options.archive_path}),

            # admin
            (r'/admin[/]?', handlers.AdminHandler),
            (r'/admin/upload', handlers.UploadHandler),
            (r'/admin/delete', handlers.DeleteHandler),

            # others
            (r'.*', handlers.IndexHandler),
        ]

        app_settings = {
            'template_path': settings.TEMPLATE_PATH,
            'static_path': settings.STATIC_PATH,
        }

        tornado.web.Application.__init__(
            self, url_handlers, **app_settings)  # pylint: disable=W0142


def main():
    '''Start web application'''

    settings.init()

    application = App()
    application.listen(options.port)  # pylint: disable=E1101
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
