from app import create_app
from flask import Flask
import gunicorn.app.base
import os
import multiprocessing
from asgiref.wsgi import WsgiToAsgi

CURRENT_ENV = os.getenv("ENVIRONMENT", "local")

class GunicornWrapper(gunicorn.app.base.BaseApplication):
    def __init__(self, app: Flask, port: int):
        threads = 2
        workers = multiprocessing.cpu_count() * 2

        self.options = {
            "bind": f"0.0.0.0:{port}",
            "workers": workers,
            "threads":threads,
            "worker_class":"uvicorn.workers.UvicornWorker"
        }

        print(f"Service Running with workers: {workers}, threads: {threads}")

        self.application = app
        super().__init__()

    def load_config(self):
        config = {k:v for k, v, in self.options.items() if k in self.cfg.settings and v is not None}

        for k, v in config.items():
            self.cfg.set(k.lower(), v )

    def load(self) -> Flask:
        print(f"Starting worker...")
        return self.application


def start_service():
    try:
        app = create_app()

        print(f"Running in {CURRENT_ENV} MODE")

        if CURRENT_ENV in ('development', 'local'):
            app.run(host="0.0.0.0", port=5000)
        else:
            print("Running Service with GUNICORN workers")
            g_app = GunicornWrapper(WsgiToAsgi(app), 5000)
            g_app.run()
    except Exception as e:
        print(f"ERROR running service: {e}")

start_service()