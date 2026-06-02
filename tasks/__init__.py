import os
import sys
from typing import List

import newrelic.agent

sys.path.insert(1, os.getcwd())

import contextlib

import database.config.db as db
import utility.logger
from database.models import StoreModel

logger = utility.logger.get_logger(__name__)


@contextlib.contextmanager
def bg_task(name):
    application = newrelic.agent.register_application(timeout=5)
    with newrelic.agent.BackgroundTask(application, name=name, group="PY/Tasks"):
        logger.info(f"BackgroundTask: {name}")
        yield


@bg_task("check-weather")
def run_task():
    logger.info("start job check-weather")
    db_session = db.get_db_session()
    stores: List[StoreModel] = db_session.query(StoreModel).all()
    logger.info(f"Found {len(stores)} stores")
    logger.info("end job check-weather")


run_task()
