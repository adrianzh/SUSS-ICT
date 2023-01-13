from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, redirect, render_template, url_for, flash
from models.form import RegistrationForm
from models.users import User

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    Reg_Form = RegistrationForm(request.form)

    if request.method == "GET":
        return render_template("register.html", RegistrationForm=Reg_Form)

    elif request.method == "POST":
        if Reg_Form.validate():
            aEmail = Reg_Form.email.data
            aPassword = Reg_Form.password.data
            aName = Reg_Form.name.data
            existing_user = User.objects(email=aEmail).first()
            if existing_user is None:
                hashpass = generate_password_hash(aPassword, method='sha256')
                new_user = User(email=aEmail, password=hashpass, name=aName).save()
                return redirect(url_for('auth.login'))
            else:
                Reg_Form.email.errors.append("User already existed")
            return render_template("register.html", RegistrationForm=Reg_Form)

        else:
            return render_template("register.html", RegistrationForm=Reg_Form) 

@auth.route("/", methods=["GET", "POST"])
@auth.route("/login", methods=["GET", "POST"])
def login():
    
    if current_user.is_authenticated == True:
        return redirect(url_for('courses.render_course'))
    else: 
        Log_Form = RegistrationForm(request.form)
        if request.method == "GET":
            return render_template("login.html", RegistrationForm=Log_Form)

        elif request.method == "POST":
            if Log_Form.validate():
                aEmail = Log_Form.email.data
                aPassword = Log_Form.password.data
                check_user = User.objects(email=aEmail).first()
                if check_user:
                    if check_password_hash(check_user['password'], Log_Form.password.data):
                        login_user(check_user)
                        return redirect(url_for('courses.render_course'))
                    else:
                        Log_Form.password.errors.append("User Password Not Correct")
                else:
                    Log_Form.email.errors.append("No Such User")
                    return render_template("login.html", RegistrationForm=Log_Form)
            else:
                return render_template("login.html", RegistrationForm=Log_Form) 

        return render_template("login.html", RegistrationForm=Log_Form)

@auth.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
