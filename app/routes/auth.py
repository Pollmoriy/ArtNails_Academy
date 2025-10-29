from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("Форма отправлена!")
        print("🔗 Текущая строка подключения:", db.engine.url)

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(f"➡ Получено: {first_name=} {last_name=} {email=} {password=} {confirm_password=}")

        # Проверка совпадения паролей
        if password != confirm_password:
            print("❌ Пароли не совпадают!")
            return "Пароли не совпадают", 400

        # Проверка существующего пользователя
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print("⚠ Пользователь с таким email уже существует")
            return "Пользователь уже существует", 400

        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=generate_password_hash(password)
            )

            db.session.add(new_user)
            db.session.commit()

            print("✅ Пользователь добавлен в БД!")
            print("📋 Список пользователей:", User.query.all())

            return redirect(url_for('profile.profile_page'))

        except Exception as e:
            print("❌ Ошибка при добавлении пользователя:", e)
            db.session.rollback()
            return "Ошибка регистрации", 500

    return render_template('register.html')



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password')

        if not all([email, password]):
            flash("Введите email и пароль", "error")
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Неверный email или пароль", "error")
            return redirect(url_for('auth.login'))

        # Авторизация успешна
        session['user_id'] = user.id_user
        flash("Вы успешно вошли!", "success")
        return redirect(url_for('profile.profile_page')) # нужно создать маршрут профиля

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('main.home'))


@auth_bp.route('/debug-users')
def debug_users():
    users = User.query.all()
    output = "<h2>Все пользователи:</h2>"
    if not users:
        output += "<p>Пока нет пользователей</p>"
    else:
        for u in users:
            output += f"<p>ID: {u.id_user}, Email: {u.email}, Имя: {u.first_name}, Фамилия: {u.last_name}</p>"
    return output
