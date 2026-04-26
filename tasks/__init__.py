import os
import sys

import newrelic.agent

sys.path.insert(1, os.getcwd())

import contextlib

import app


@contextlib.contextmanager
def bg_task(name):
    application = newrelic.agent.register_application(timeout=5)
    with newrelic.agent.BackgroundTask(application, name=name, group="PY/Tasks"):
        print(f"BackgroundTask: {name}")
        yield


@bg_task("check-weather")
def run_task():
    print("Hello world from check-weather")


run_task()
