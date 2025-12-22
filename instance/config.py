from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://artnails_user:artnails123@localhost/artnails_academy'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'supersecretkey'  # обязательно!
PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # или timedelta(hours=8) — как хочешь
GOOGLE_CLIENT_ID = "992264053540-8b525cedqlcrhbdj4f6j5hotas10026g.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

