from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Загружаем настройки из instance/config.py
    app.config.from_pyfile('config.py')

    db.init_app(app)

    # ⚠️ Обязательно импортируем все модели
    from . import models

    # Создаём таблицы
    with app.app_context():
        db.create_all()
        print("✅ Таблицы успешно созданы или уже существуют.")

    return app
