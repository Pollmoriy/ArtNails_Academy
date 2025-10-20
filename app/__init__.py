from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Загружаем настройки из instance/config.py
    app.config.from_pyfile('config.py', silent=False)

    # Инициализация базы данных
    db.init_app(app)

    # Импорт моделей (важно делать после инициализации db)
    from . import models

    # Создаём таблицы, если их ещё нет
    with app.app_context():
        db.create_all()
        print("✅ Таблицы успешно созданы или уже существуют.")

    # Можно позже подключить маршруты
    # from .routes import main_bp
    # app.register_blueprint(main_bp)

    return app


