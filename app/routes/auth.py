from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, template_folder='../templates')


# -------------------- РЕГИСТРАЦИЯ --------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Если пользователь уже авторизован — не пускаем на регистрацию
    if 'user_id' in session:
        return redirect(url_for('profile.profile_page'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # ---- Проверка заполнения полей ----
        if not all([first_name, last_name, email, password, confirm_password]):
            flash("Заполните все поля", "error")
            return redirect(url_for('auth.register'))

        # ---- Проверка совпадения паролей ----
        if password != confirm_password:
            flash("Пароли не совпадают", "error")
            return redirect(url_for('auth.register'))

        # ---- Проверка длины пароля ----
        if len(password) < 6:
            flash("Пароль должен быть не менее 6 символов", "error")
            return redirect(url_for('auth.register'))

        # ---- Проверка существующего пользователя ----
        if User.query.filter_by(email=email).first():
            flash("Пользователь с таким email уже существует", "error")
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

            # ---- Авторизуем пользователя сразу после регистрации ----
            session['user_id'] = new_user.id_user
            session.permanent = True

            flash("Регистрация прошла успешно!", "success")
            return redirect(url_for('profile.profile_page'))

        except Exception as e:
            db.session.rollback()
            flash("Ошибка при регистрации. Попробуйте позже.", "error")
            return redirect(url_for('auth.register'))

    return render_template('register.html')


# -------------------- ВХОД --------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже авторизован — не пускаем на логин
    if 'user_id' in session:
        return redirect(url_for('profile.profile_page'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')

        if not all([email, password]):
            flash("Введите email и пароль", "error")
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Неверный email или пароль", "error")
            return redirect(url_for('auth.login'))

        # ---- Успешный вход ----
        session['user_id'] = user.id_user
        session.permanent = True

        flash("Вы успешно вошли!", "success")
        return redirect(url_for('profile.profile_page'))

    return render_template('login.html')


# -------------------- ВЫХОД --------------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('main.home'))
