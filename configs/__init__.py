redis_config = {'host': '', 'port': 6739, 'db': 0}

umeng_config = {'username': '', 'password': ''}

celery_config = {
    'BROKER_URL': 'amqp://guest@localhost/',
    'BROKER_POOL_LIMIT': 256,
    'CELERY_RESULT_BACKEND': "redis://localhost/0",
    'CELERY_REDIS_MAX_CONNECTIONS': 512,
    'CELERY_ACCEPT_CONTENT': ['pickle', 'json', 'msgpack'],
    'CELERY_TASK_SERIALIZER': "json",
    'CELERY_RESULT_SERIALIZER': "json",
    'CELERY_TIMEZONE': 'Asia/Shanghai',
    'CELERY_ENABLE_UTC': True,
    'CELERYD_LOG_FORMAT':
    '%(asctime)s %(levelname)-2s %(name)s.%(funcName)s:%(lineno)-5d %(message)s',
    'CELERYD_TASK_LOG_FORMAT':
    '%(asctime)s %(levelname)-2s %(name)s.%(funcName)s:%(lineno)-5d %(message)s %(task_name)s(%(task_id)s) %(message)s',
    'CELERY_ACKS_LATE': True,
    'CELERYD_PREFETCH_MULTIPLIER': 16,
    'CELERY_ROUTES': {'syb_test_wrapper': {'queue': 'syb_test'}},
    'CELERY_TASK_RESULT_EXPIRES': 900,
    'CELERY_DISABLE_RATE_LIMITS': True
}
