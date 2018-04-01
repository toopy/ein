from functools import wraps


def merge_config_and_data(runner):
    @wraps(runner)
    async def wrapper(self, event):
        kwargs = dict(
            self.config,
            **(event.data.get('config', None) or {})
        )
        return await runner(self, event, **kwargs)
    return wrapper
