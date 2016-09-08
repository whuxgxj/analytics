#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement

import redis
from rq import Worker, Queue, Connection
from configs import redis_config

redis_url = 'redis://' + redis_config.get('host') + ':' + redis_config.get(
    'port')
redis_conn = redis.from_url(redis_url)

queue_high = Queue('high', connection=redis_conn)
queue_normal = Queue('normal', connection=redis_conn)
queue_low = Queue('low', connection=redis_conn)

redis_db = redis.StrictRedis(**redis_config)

if __name__ == '__main__':
    # start a worker
    with Connection(redis_conn):
        worker = Worker(map(Queue, ['high', 'normal', 'low']))
        worker.work()
