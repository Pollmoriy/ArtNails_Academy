from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://artnails_user:artnails123@localhost/artnails_academy'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'supersecretkey'  # обязательно!
PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # или timedelta(hours=8) — как хочешь
