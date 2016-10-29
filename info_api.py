# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import define, options
import pymongo
import settings
from tornado.web import asynchronous
import tornado.gen
import json
import os

define("port", default=9998, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/api/country', CodeHandler),
            (r'/api/android', AndroidHandler),
            (r'/country', CoHandler),
            (r'/android', AnHandler),
            (r'/operate', OperateHandler),
            (r'/country/op', OpCountryHandler),
            (r'/android/op', OpAndroidHandler),
        ]
        setting = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        super(Application, self).__init__(handlers, **setting)
        conn = pymongo.Connection(
            settings.MONGODB_HOST,
            settings.MONGODB_PORT
        )
        db = conn[settings.MONGODB_DB]
        self.code = db[settings.CODE_INFO]
        self.android = db[settings.ANDROID_INFO]


class BaseHandler(tornado.web.RequestHandler):
    @property
    def co(self):
        return self.application.code

    @property
    def an(self):
        return self.application.android


class CodeHandler(BaseHandler):
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument('code')
        country = self.co.find_one({'code': code})
        if country:
            country.pop('_id')
        else:
            country = {'status': 'no data'}
        self.write(json.dumps(country, ensure_ascii=False))


class AndroidHandler(BaseHandler):
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        api = self.get_argument('api')
        version = self.an.find_one({'api': api})
        if version:
            version.pop('_id')
        else:
            version = {'status':'no data'}
        self.write(json.dumps(version, ensure_ascii=False))


class CoHandler(BaseHandler):
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        values = self.co.find()
        self.render("country.html", values=values)


class AnHandler(BaseHandler):
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        values = self.an.find()
        self.render("android.html", values=values)


class OperateHandler(BaseHandler):
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.render("operate.html")


class OpCountryHandler(BaseHandler):
    @asynchronous
    @tornado.gen.coroutine
    def post(self):
        code = self.get_argument("code")
        en = self.get_argument("en")
        cn = self.get_argument("cn")
        self.co.update({'code': code}, {'code': code, 'en': en, 'cn': cn}, upsert=True)
        self.redirect("/country")


class OpAndroidHandler(BaseHandler):
    @asynchronous
    @tornado.gen.coroutine
    def post(self):
        api = self.get_argument("api")
        version = self.get_argument("version")
        name = self.get_argument("name")
        self.an.update({'api': api}, {'api': api, 'version': version, 'name': name}, upsert=True)
        self.redirect("/android")

if __name__ == "__main__":
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print "Application starts on port: ", options.port
    tornado.ioloop.IOLoop.instance().start()



