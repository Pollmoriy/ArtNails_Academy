from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import stripe
import os
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    # ✅ Stripe
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_51Sh4Tc1jz8KwkjqINnBmQmRQEtR7gkKP09pb2qTbp18lOPxpxdEgu7ySaCjyUmgu2BUJbMS6wRn5opzpJduwdygo00TYAGFDjN'
    app.config['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_51Sh4Tc1jz8KwkjqIAOuq3v76o8Klf3EIZ8HXTkUMithm1REOx858elF2aHcpP75X5iINXgl5SAuk2uviiApwE5IL00VIyMkIqr'

    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    app.secret_key = "super_secret_key_123"
    app.permanent_session_lifetime = timedelta(days=7)

    db.init_app(app)

    # 🔹 Регистрация блюпринтов
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.profile import profile_bp
    from app.routes.about import about_bp
    from app.routes.catalog import catalog_bp
    from app.routes.course_desk import course_desk_bp
    from app.routes.enroll import enroll_bp
    from app.routes.course import course_bp
    from app.routes.test import test_bp
    app.register_blueprint(test_bp)

    app.register_blueprint(course_bp)
    app.register_blueprint(enroll_bp)
    app.register_blueprint(course_desk_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(catalog_bp)

    oauth.init_app(app)

    @app.context_processor
    def inject_user_status():
        user_id = session.get('user_id')
        return {
            'user_logged_in': bool(user_id)
        }

    return app
