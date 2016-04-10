from flask.ext.script import Server, Manager, Shell
from config import Config
from app import create_app

app = create_app()
manager = Manager(app)
manager.add_command(
    "runserver",
    Server(host=Config.HOST, port=Config.PORT)
)

if __name__ == '__main__':
    manager.run()
