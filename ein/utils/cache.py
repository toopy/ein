from aiocache import caches
from decouple import config


def setup_cache():
    cache_cls = config('CACHE_CLS', default='SimpleMemoryCache')

    if cache_cls == 'RedisCache':
        extra = {
            'db': config('CACHE_REDIS_DB', cast=int, default=0),
            'endpoint': config('CACHE_REDIS_HOST', default='127.0.0.1'),
            'port': config('CACHE_REDIS_PORT', cast=int, default=6379),
        }
    else:
        extra = {}

    caches.set_config({
        'default': dict(
            {
                'cache': f'aiocache.{cache_cls}',
                'serializer': {
                    'class': "aiocache.serializers.JsonSerializer",
                },
            },
            **extra,
        ),
    })
