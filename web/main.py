#-*- coding:utf-8 -*-
import os
import sys
from logger import logger
from getopt import getopt,GetoptError

from pymongo import MongoClient
from ConfigParser import SafeConfigParser

from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

from url import handlers


config_path = os.path.join(os.path.dirname(__file__),'config.conf')

config = SafeConfigParser()
config.read(config_path)


class App(web.Application):
    def __init__(self):
        settings = dict(
                debug = False,
                cookie_secret = "asdasfsdjf#8899",
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies = False
                )
        mongo = MongoClient(config.get('mongodb','host'), config.getint("mongodb","port"))
        self.db = mongo.xinrui
        super(App, self).__init__(handlers, **settings)

try:
    options,args = getopt(sys.argv[1:],"port:",["port="])
except GetoptError,e:
    logger.fatal(e)

port = 8080
for option in options:
    if option[0] == "--port":
        port = int(option[1])
        break

http_server = HTTPServer(App(), xheaders=True)
http_server.bind(port)
http_server.start(1)
logger.info("http server start on port %s..." % port)
IOLoop.instance().start()

