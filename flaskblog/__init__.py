import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cd9c32ed54b0653c0fe312cee044f505'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
from flask_admin import Admin
from flaskblog.admin_views import SecureModelView
from flaskblog.models import User, Post

admin = Admin(app, name='Admin Panel')
admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Post, db.session))