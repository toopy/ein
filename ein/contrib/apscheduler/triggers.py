from apscheduler.triggers.base import BaseTrigger


class NowTrigger(BaseTrigger):

    def __init__(self, timezone=None):
        pass

    def get_next_fire_time(self, previous_fire_time, now):
        return now if previous_fire_time is None else None
