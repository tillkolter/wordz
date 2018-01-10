import os

__author__ = 'tkolter'


class Config:

    DEBUG = False
    TESTING = False
    REDIS_URL = 'redis://{host}:6379/0'.format(
        host=os.environ.get('REDIS_HOST', 'redis')
    )
    MORPHOLOGY_FILE = os.environ.get('MORPHOLOGY_FILE', '/data/dictionary.dump')
