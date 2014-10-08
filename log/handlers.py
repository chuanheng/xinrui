#-*-coding:utf-8
from datetime import datetime
import logging
import socket
import redis
import json

class MongoFormatter(logging.Formatter):

    DEFAULT_PROPERTIES = logging.LogRecord('', '', '', '', '', '', '', '').__dict__.keys()

    def format(self, record):
        """Formats LogRecord into python dictionary."""
        # Standard document
        document = {
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'level': record.levelname,
            'thread': record.thread,
            'threadName': record.threadName,
            'message': record.getMessage(),
            'loggerName': record.name,
            'fileName': record.pathname,
            'module': record.module,
            'method': record.funcName,
            'lineNumber': record.lineno,
            'hostname': socket.getfqdn(socket.gethostname()),
            'ip': socket.gethostbyname(socket.gethostname())
        }
        # Standard document decorated with exception info
        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })
        # Standard document decorated with extra contextual information
        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]
        return document


class RedisHandler(logging.Handler):
    
    def __init__(self, host='localhost', port=6379, db=0, list='logs'):
        
        logging.Handler.__init__(self, 0)
        self.host = host
        self.port = port
        self.db = db
        self.list = list
        self.r = None
        self.formatter = MongoFormatter()
        self._connect()
    
    def _connect(self):
        """Connecting to redis database."""
        try: 
            self.r = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
        except:
            raise
    
    def close(self):
        pass
    
    def emit(self, record):
        """Inserting new logging record to redis message list."""
        if self.list is not None:
            try:
                self.r.lpush(self.list, json.dumps(self.format(record)))
            except Exception:
                self.handleError(record)
    
    
    
