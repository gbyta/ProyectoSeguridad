from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.user import User
from forms.user_forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Configuración de Clave Secreta y Cookies de Sesión
app.config['SECRET_KEY'] = 'clave_super_secreta'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

# Inicialización de protecciones y manejador de login
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.get_by_username(form.username.data):
            flash('El nombre de usuario ya está registrado.')
            return render_template('register.html', form=form)
        
        User.create(form.username.data, form.password.data)
        flash('Registro exitoso. ¡Ahora puedes iniciar sesión!')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Has iniciado sesión correctamente.')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('profile'))
        else:
            flash('Credenciales inválidas.')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Manejadores de errores 401 y 403
@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('401.html'), 401

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)