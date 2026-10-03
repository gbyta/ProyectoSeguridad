from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message="El nombre de usuario es obligatorio."),
        Length(min=3, max=25, message="El usuario debe tener entre 3 y 25 caracteres.")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message="Por favor confirma tu contraseña."),
        EqualTo('password', message="Las contraseñas no coinciden.")
    ])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message="El nombre de usuario es obligatorio.")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria.")
    ])
    submit = SubmitField('Iniciar Sesión')