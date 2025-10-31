from datetime import datetime
from app import db

# 🧑‍🎓 Пользователь
class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(255))
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"


# 🎓 Курсы
class Course(db.Model):
    __tablename__ = 'courses'

    id_course = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.Integer, db.ForeignKey('teachers.id_teacher'))
    title = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    price = db.Column(db.Numeric(10, 2), default=0.00)
    duration_weeks = db.Column(db.Integer)
    difficulty = db.Column(db.Enum('Начинающий', 'Средний', 'Продвинутый'))
    status = db.Column(db.Enum('purchased', 'completed'), default='purchased')

    # связь с преподавателем
    teacher = db.relationship('Teacher', back_populates='courses')

    def __repr__(self):
        return f"<Course {self.title}>"


# 👩‍🏫 Преподаватели
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id_teacher = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    photo = db.Column(db.String(255))

    # связь с курсами
    courses = db.relationship('Course', back_populates='teacher')

    def __repr__(self):
        return f"<Teacher {self.first_name} {self.last_name}>"

