import asyncio
import logging

from tukio import Engine
from tukio import WorkflowTemplate

from .utils.config import read_config


logger = logging.getLogger(__name__)


class Workflow:

    def __init__(self, config):
        self.config = config

    async def run(self, **kw):
        engine = Engine()

        workflow_tmpl = WorkflowTemplate.from_dict(self.config)
        await engine.load(workflow_tmpl)

        task = await engine.data_received(kw or {})
        task_uid = task[0].uid

        logger.debug(f'Task {task_uid} start')
        await asyncio.wait(task)
        logger.debug(f'Task {task_uid} ended')

    @staticmethod
    async def from_config_path(config_path):
        workflow_config = await read_config(config_path)
        return Workflow(workflow_config)
