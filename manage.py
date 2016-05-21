#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config

from flask.ext.script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app

app = create_app()

migrate = Migrate(app, app.db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
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
