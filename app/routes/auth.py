from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, oauth
from app.models import User
import secrets

auth_bp = Blueprint('auth', __name__, template_folder='../templates')


# ==================== GOOGLE OAUTH ====================

google = oauth.register(
    name='google',
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/',
    client_kwargs={'scope': 'email profile'}
)


@auth_bp.route('/login/google')
def login_google():
    session['google_mode'] = 'login'
    redirect_uri = url_for('auth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route('/register/google')
def register_google():
    session['google_mode'] = 'register'
    redirect_uri = url_for('auth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route('/auth/google/callback')
def google_callback():
    mode = session.pop('google_mode', 'login')

    try:
        token = google.authorize_access_token()
        resp = google.get('oauth2/v2/userinfo', token=token)
        user_info = resp.json()
    except Exception:
        session['oauth_error'] = "Ошибка авторизации через Google. Попробуйте позже."
        return redirect(url_for('auth.login'))

    email = user_info.get('email')
    first_name = user_info.get('given_name', 'Пользователь')
    last_name = user_info.get('family_name', 'Google')
    avatar = user_info.get('picture')

    if not email:
        session['oauth_error'] = "Не удалось получить email из Google. Попробуйте другой аккаунт."
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if mode == 'login':
        if not user:
            session['oauth_error'] = "Аккаунт с таким Google не найден. Зарегистрируйтесь."
            return redirect(url_for('auth.register'))

    if mode == 'register':
        if user:
            session['oauth_error'] = "Аккаунт с таким Google уже существует. Войдите."
            return redirect(url_for('auth.login'))

        try:
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                avatar=avatar,
                password_hash=generate_password_hash(secrets.token_hex(16))
            )
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            session['oauth_error'] = "Ошибка при регистрации через Google. Попробуйте позже."
            return redirect(url_for('auth.register'))

    session['user_id'] = user.id_user
    session.permanent = True

    flash("Вы успешно вошли через Google", "success")
    return redirect(url_for('profile.profile_page'))


# ==================== Обычная регистрация ====================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        flash("Вы уже авторизованы.", "info")
        return redirect(url_for('profile.profile_page'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([first_name, last_name, email, password, confirm_password]):
            flash("Заполните все поля.", "error")
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash("Пароли не совпадают.", "error")
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash("Пароль должен быть не менее 6 символов.", "error")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash("Пользователь с таким email уже существует.", "error")
            return redirect(url_for('auth.register'))

        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id_user
            session.permanent = True

            flash("Регистрация прошла успешно!", "success")
            return redirect(url_for('profile.profile_page'))
        except Exception:
            db.session.rollback()
            flash("Ошибка при регистрации. Попробуйте позже.", "error")
            return redirect(url_for('auth.register'))

    return render_template('register.html')


# ==================== Обычный вход ====================

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash("Вы уже авторизованы.", "info")
        return redirect(url_for('profile.profile_page'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')

        if not all([email, password]):
            flash("Введите email и пароль.", "error")
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Неверный email или пароль.", "error")
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id_user
        session.permanent = True

        flash("Вы успешно вошли!", "success")
        return redirect(url_for('profile.profile_page'))

    return render_template('login.html')


# ==================== Выход ====================

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Вы вышли из аккаунта.", "success")
    return redirect(url_for('main.home'))
