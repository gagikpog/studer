from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from config import Config
from flask_script import Manager
from flask_login import LoginManager
from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore #Хранилище данных SQLAlchemy
from flask_security import Security
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
app.secret_key = 'xxxxyyyyyzzzzz'
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# manager=Manager(app)
# manager.add_command('db',MigrateCommand)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import models
from app.routes import user_route, routes, bill_route, auth_route
from app.routes import file_loader

#администрирование- продумать позже
### ADMIN ###
#from models import *
#admin = Admin(app)
#admin.add_view(ModelView())

### Flask-security ###
# from app.models import User, Role
# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)
