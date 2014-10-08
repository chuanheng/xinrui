# -*- coding:utf-8 -*-
import os
import time
from datetime import datetime
import getopt
import ConfigParser

from logger import logger
from pymongo import MongoClient
from getopt import getopt,GetoptError
import redis
import json

root_path = os.path.dirname(__file__)
config_path = os.path.join(root_path,'config.conf')
logger.info("Serivce Start.loading config path:%s" % config_path)
config = ConfigParser.SafeConfigParser()
config.read(config_path)

r = redis.StrictRedis(host=config.get('redis','host'), port=config.get('redis','port'), db=1)

mongo = MongoClient("mongodb://%s" % config.get('mongodb','host'))
db = mongo.xinrui

while 1:
    message = r.rpop('logs')
    print message
    if not message:
        time.sleep(2)
        continue
    
    message = json.loads(message)
    collection_name = message['loggerName'] # 用loggerName做 mongo中的表名
    
    message['created_at'] = datetime.strptime(message['created_at'], '%Y-%m-%d %H:%M:%S.%f')
    # 写入 mongo
    getattr(db, collection_name).insert(message)
    


