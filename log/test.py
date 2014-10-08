#-*-coding:utf-8

import logging
from handlers import RedisHandler

logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger('redis_log') # mongo中的表名，一个Logger一个表
log.addHandler(RedisHandler(host='127.0.0.1', port=6379, db=1, list='logs')) #redis配置信息
# log.warning('Hello world!log test')
# 额外的字段放在 extra 中，同样存入 mongo表中
log.critical("额外的字段放在 extra 中，同样存入 mongo表中",extra={'extra':'extra'})


