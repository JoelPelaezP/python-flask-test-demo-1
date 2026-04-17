#!/bin/sh

flask db upgrade

exec python __main__.py

#exec flask run --host 0.0.0.0 