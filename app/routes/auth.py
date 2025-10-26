from flask import Blueprint, render_template, redirect, url_for, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Тут позже добавим проверку пользователя
        return redirect(url_for('main.home'))

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
