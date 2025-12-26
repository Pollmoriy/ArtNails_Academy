from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://artnails_user:artnails123@localhost:3306/artnails_academy'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'supersecretkey'
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
