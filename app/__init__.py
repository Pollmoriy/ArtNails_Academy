from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    # 🔹 Проверим подключение к базе данных
    with app.app_context():
        try:
            engine = db.engine
            conn = engine.connect()
            db_name = conn.execute(db.text("SELECT DATABASE();")).scalar()
            print(f"✅ Подключение к MySQL успешно! Используемая БД: {db_name}")
            conn.close()
        except Exception as e:
            print("❌ Ошибка подключения к базе данных!")
            print(e)

    # 🔹 Импорт моделей (чтобы SQLAlchemy знал о них)
    from . import models

    # 🔹 Импорт и регистрация Blueprint’ов
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app

