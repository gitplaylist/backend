#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server, Shell
from flask_migrate import MigrateCommand

from app import create_app
from config import Config

app = create_app()
manager = Manager(app)
manager.add_command(
    "runserver",
    Server(host=Config.HOST, port=Config.PORT)
)
manager.add_command(
    'migrate',
    MigrateCommand
)

if __name__ == '__main__':
    manager.run()
