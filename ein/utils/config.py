import json
import os.path

import aiofiles


def cast_list(value):
    return filter(None, [s.strip() for s in value.split(',')])


async def read_config(path):
    if not os.path.exists(path):
        raise RuntimeError(f'Config not found: {path}')

    async with aiofiles.open(path) as f:
        return json.loads(await f.read())
