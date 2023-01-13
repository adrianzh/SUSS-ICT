from wtforms import Form, StringField, validators, PasswordField

class RegistrationForm(Form):
    email = StringField('Email', \
        [validators.InputRequired(), validators.email(message="Invalid email"), \
            validators.Length(max=30, message="Field cannot be longer than 30 characters.")])
    password = PasswordField('Passsword', \
        [validators.Length(min=5, max=20, message="Field must be bebetween 5 and 20 charcaters long.")])
    name = StringField('Name')
