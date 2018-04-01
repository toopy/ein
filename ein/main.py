import asyncio
import logging
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from decouple import config

from .job import Job
from .utils.cache import setup_cache
from .utils.config import cast_list
from .utils.config import read_config
from .utils.logging import setup_logging


logger = logging.getLogger(__name__)


def register_tasks_modules():
    for tasks_module in config('TASKS', cast=cast_list, default=''):
        logger.debug('registering tasks from: %s', tasks_module)
        __import__(tasks_module)


async def register_jobs(loop, scheduler):
    for path in config('JOBS', cast=cast_list, default=''):
        logger.debug('registering jobs from: %s', path)
        for job_config in (await read_config(path)):
            await Job(job_config).register(scheduler)


def run():
    setup_cache()
    setup_logging()

    loop = asyncio.get_event_loop()

    scheduler = AsyncIOScheduler()
    scheduler.configure(timezone=config('TIMEZONE', default='UTC'))

    err_found = False
    try:
        register_tasks_modules()
        loop.run_until_complete(register_jobs(loop, scheduler))
        scheduler.start()
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except RuntimeError as e:
        err_found = True
        sys.stderr.write(f'{e}\n')
    finally:
        scheduler.shutdown(wait=not err_found)

    if err_found:
        sys.exit(1)
