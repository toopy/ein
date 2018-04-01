import logging

from .workflow import Workflow

logger = logging.getLogger(__name__)


class Job:

    _workflow = None

    def __init__(self, config):
        self.config = config
        self.kwargs_list = self.config.pop('kwargs', None) or [{}]
        self.workflow_path = self.config.pop('workflow')

    @property
    async def workflow(self):
        if self._workflow is None:
            self._workflow = await Workflow.from_config_path(
                self.workflow_path
            )
        return self._workflow

    async def register(self, scheduler):
        for kwargs in self.kwargs_list:
            scheduler.add_job(
                (await self.workflow).run,
                kwargs=kwargs,
                **self.config
            )
