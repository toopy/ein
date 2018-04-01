from __future__ import absolute_import
import logging.config

from decouple import config

from .config import cast_list


def setup_logging():

    if config('VERBOSE', cast=bool, default=True):
        fmt = '%(asctime)s %(levelname)-8s %(name)s.%(funcName)s:%(lineno)-3d "%(message)s"'  # noqa
        level = 'DEBUG'
    else:
        fmt = '%(asctime)s %(message)s'
        level = 'INFO'

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'datefmt': '%H:%M',
                'format': fmt,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            l: {'level': level}
            for l in config('LOGGERS', cast=cast_list, default='ein')
        },
        'root': {
            'handlers': ['console'],
        },
    })
