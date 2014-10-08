# -*-coding:utf-8 -*-
from utils.handler import BaseHandler

class MainHandler(BaseHandler):
    def get(self):
        loggerName = self.get_argument("loggerName", default='redis_log')
        level = self.get_argument("level", default='')
        status = int(self.get_argument("status", default=-1) )
        
        spec = {}
        if level:
            spec.update({'level':level})
        if status!=-1:
            spec.update({'status':status})
        
        logs = getattr(self.db, loggerName).find(spec).sort('created_at', -1)
        
        list = []
        for log in logs:
            log['created_at'] = log['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            log['status'] = log['status'] if 'status' in log else ''
            log['ip'] = log['ip'] if 'ip' in log else ''
            list.append(log)
        
        loggerNames = ['redis_log','test','root']
        levels = ["DEBUG","INFO","WARNING","ERROR","CRITICAL","FATAL"]
        status_list = [0,1,2,3]
        
        self.render("index.html",
                    logs=list,
                    loggerNames=loggerNames,loggerName=loggerName,
                    levels=levels,level=level,
                    status_list=status_list,status=status,
                    )
    
    def post(self):
        self.get()
    
handlers = [
        (r"/", MainHandler)
        ]



