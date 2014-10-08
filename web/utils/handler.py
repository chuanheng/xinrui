#-*-coding:utf-8 -*-
from tornado.web import RequestHandler
import os.path
import tornado.ioloop
import mako.lookup
import tornado.httpserver
import mako.template

class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)
        self.db = self.application.db

    def write(self, chunk):
        super(BaseHandler, self).write(chunk)
        #run time
    
    # mako
    def initialize(self):
        template_path = self.get_template_path()
        print "template_path",template_path
        self.lookup = mako.lookup.TemplateLookup(directories=[template_path], input_encoding='utf-8', output_encoding='utf-8')
    
    def render_string(self, template_path, **kwargs):
        template = self.lookup.get_template(template_path)
        print template
        namespace = self.get_template_namespace()
        namespace.update(kwargs)
        return template.render(**namespace)
    
    def render(self, template_path, **kwargs):
        self.finish(self.render_string(template_path, **kwargs))
    
