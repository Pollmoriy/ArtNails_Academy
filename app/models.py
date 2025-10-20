from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ==========================================================
#                     ПОЛЬЗОВАТЕЛИ
# ==========================================================
class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(255))  # путь к файлу
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    # связи
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    purchases = db.relationship('Purchase', back_populates='user', cascade="all, delete-orphan")
    certificates = db.relationship('Certificate', back_populates='user', cascade="all, delete-orphan")
    progress = db.relationship('Progress', back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


# ==========================================================
#                     ПРЕПОДАВАТЕЛИ
# ==========================================================
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id_teacher = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(150))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    photo = db.Column(db.String(255))

    # связь с курсами
    courses = db.relationship('Course', back_populates='teacher', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Teacher {self.first_name} {self.last_name}>"


# ==========================================================
#                        КУРСЫ
# ==========================================================
class Course(db.Model):
    __tablename__ = 'courses'

    id_course = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text)
    image = db.Column(db.String(255))
    difficulty = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    duration_weeks = db.Column(db.Integer)
    id_teacher = db.Column(db.Integer, db.ForeignKey('teachers.id_teacher'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # связи
    teacher = db.relationship('Teacher', back_populates='courses')
    details = db.relationship('CourseDetail', back_populates='course', uselist=False, cascade="all, delete-orphan")
    modules = db.relationship('Module', back_populates='course', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='course', cascade="all, delete-orphan")
    purchases = db.relationship('Purchase', back_populates='course', cascade="all, delete-orphan")
    certificates = db.relationship('Certificate', back_populates='course', cascade="all, delete-orphan")
    progress = db.relationship('Progress', back_populates='course', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course {self.title}>"


# ==========================================================
#                ДЕТАЛИ О КУРСЕ (ОПИСАНИЕ)
# ==========================================================
class CourseDetail(db.Model):
    __tablename__ = 'course_details'

    id_details = db.Column(db.Integer, primary_key=True)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'), unique=True)
    full_description = db.Column(db.Text)
    learning_outcomes = db.Column(db.Text)
    requirements = db.Column(db.Text)

    course = db.relationship('Course', back_populates='details')

    def __repr__(self):
        return f"<CourseDetail {self.id_course}>"


# ==========================================================
#                         МОДУЛИ
# ==========================================================
class Module(db.Model):
    __tablename__ = 'modules'

    id_module = db.Column(db.Integer, primary_key=True)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    type = db.Column(db.String(50))  # теория / практика / тест
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer)
    video_link = db.Column(db.String(255))
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id_test'))

    course = db.relationship('Course', back_populates='modules')
    materials = db.relationship('Material', back_populates='module', cascade="all, delete-orphan")
    practice_stages = db.relationship('PracticeStage', back_populates='module', cascade="all, delete-orphan")
    test = db.relationship('Test', back_populates='module')

    def __repr__(self):
        return f"<Module {self.title}>"


# ==========================================================
#                     ДОПОЛНИТЕЛЬНЫЕ МАТЕРИАЛЫ
# ==========================================================
class Material(db.Model):
    __tablename__ = 'materials'

    id_material = db.Column(db.Integer, primary_key=True)
    id_module = db.Column(db.Integer, db.ForeignKey('modules.id_module'))
    file_name = db.Column(db.String(255))
    file_link = db.Column(db.String(255))

    module = db.relationship('Module', back_populates='materials')


# ==========================================================
#                   ЭТАПЫ ПРАКТИКИ
# ==========================================================
class PracticeStage(db.Model):
    __tablename__ = 'practice_stages'

    id_stage = db.Column(db.Integer, primary_key=True)
    id_module = db.Column(db.Integer, db.ForeignKey('modules.id_module'))
    step_number = db.Column(db.Integer)
    step_description = db.Column(db.Text)
    image = db.Column(db.String(255))

    module = db.relationship('Module', back_populates='practice_stages')


# ==========================================================
#                         ТЕСТЫ
# ==========================================================
class Test(db.Model):
    __tablename__ = 'tests'

    id_test = db.Column(db.Integer, primary_key=True)
    id_module = db.Column(db.Integer, db.ForeignKey('modules.id_module'))
    title = db.Column(db.String(255))
    passing_score = db.Column(db.Integer)

    module = db.relationship('Module', back_populates='test')
    questions = db.relationship('Question', back_populates='test', cascade="all, delete-orphan")


# ==========================================================
#                        ВОПРОСЫ
# ==========================================================
class Question(db.Model):
    __tablename__ = 'questions'

    id_question = db.Column(db.Integer, primary_key=True)
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id_test'))
    question_text = db.Column(db.Text, nullable=False)

    test = db.relationship('Test', back_populates='questions')
    answers = db.relationship('Answer', back_populates='question', cascade="all, delete-orphan")


# ==========================================================
#                         ОТВЕТЫ
# ==========================================================
class Answer(db.Model):
    __tablename__ = 'answers'

    id_answer = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer, db.ForeignKey('questions.id_question'))
    answer_text = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)

    question = db.relationship('Question', back_populates='answers')


# ==========================================================
#                         ОТЗЫВЫ
# ==========================================================
class Review(db.Model):
    __tablename__ = 'reviews'

    id_review = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    rating = db.Column(db.Integer)
    text = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='reviews')
    course = db.relationship('Course', back_populates='reviews')


# ==========================================================
#                       ПОКУПКИ
# ==========================================================
class Purchase(db.Model):
    __tablename__ = 'purchases'

    id_purchase = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_link = db.Column(db.String(255))
    status = db.Column(db.String(50))  # например: 'оплачено', 'ожидание', 'отменено'

    user = db.relationship('User', back_populates='purchases')
    course = db.relationship('Course', back_populates='purchases')


# ==========================================================
#                     ПРОГРЕСС ПРОХОЖДЕНИЯ
# ==========================================================
class Progress(db.Model):
    __tablename__ = 'progress'

    id_progress = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    completed_modules = db.Column(db.Integer, default=0)
    total_modules = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='progress')
    course = db.relationship('Course', back_populates='progress')


# ==========================================================
#                        СЕРТИФИКАТЫ
# ==========================================================
class Certificate(db.Model):
    __tablename__ = 'certificates'

    id_certificate = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(255))

    user = db.relationship('User', back_populates='certificates')
    course = db.relationship('Course', back_populates='certificates')
