from flask_login import login_required, current_user
from flask import render_template, request
from app import app, db, login_manager

# Register Blueprint so we can factor routes
from controllers.auth import auth
app.register_blueprint(auth)

from controllers.course import course
app.register_blueprint(course)

from controllers.dashboard import dashboard
app.register_blueprint(dashboard)

#import users
from models.users import User

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/base')
def show_base():
    return render_template('base.html')