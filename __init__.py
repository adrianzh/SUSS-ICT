from flask import Flask
from flask_mongoengine import MongoEngine, Document
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    
    app.config['MONGODB_SETTINGS'] = {
        'db':'ict239tma',
        'host':'localhost'
    }
    app.static_folder = 'assets'
    db = MongoEngine(app)
    app.config['SECRET_KEY'] = 'adrianNgorTMAict239'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    return app, db, login_manager

app, db, login_manager = create_app()