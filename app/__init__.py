from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    # 🔹 Ключ для шифрования cookie
    app.secret_key = "super_secret_key_123"

    # 🔹 Настройки сессии
    app.permanent_session_lifetime = timedelta(days=7)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False

    db.init_app(app)

    # 🔹 Регистрация блюпринтов
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.profile import profile_bp
    from app.routes.about import about_bp
    from app.routes.catalog import catalog_bp
    from app.routes.course_desk import course_desk_bp
    from app.routes.enroll import enroll_bp

    app.register_blueprint(enroll_bp)
    app.register_blueprint(course_desk_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(catalog_bp)

    @app.context_processor
    def inject_user_status():
        user_id = session.get('user_id')
        return {
            'user_logged_in': bool(user_id)
        }

    return app
