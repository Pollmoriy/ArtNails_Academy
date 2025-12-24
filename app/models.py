from datetime import datetime
from app import db
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.mysql import JSON
# ===================== Пользователи =====================
class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(255))
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('Review', back_populates='user')
    purchases = db.relationship('Purchase', back_populates='user')
    progress = db.relationship('Progress', back_populates='user')
    certificates = db.relationship('Certificate', back_populates='user')

    def __repr__(self):
        return f"<User {self.email}>"


# ===================== Преподаватели =====================
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id_teacher = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    photo = db.Column(db.String(255))

    courses = db.relationship('Course', back_populates='teacher')

    def __repr__(self):
        return f"<Teacher {self.first_name} {self.last_name}>"


# ===================== Курсы =====================
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

    teacher = db.relationship('Teacher', back_populates='courses')
    modules = db.relationship('Module', back_populates='course')
    reviews = db.relationship('Review', back_populates='course')
    purchases = db.relationship('Purchase', back_populates='course')
    progress = db.relationship('Progress', back_populates='course')
    certificates = db.relationship('Certificate', back_populates='course')
    details = db.relationship('CourseDetail', back_populates='course', uselist=False)

    def __repr__(self):
        return f"<Course {self.title}>"


# ===================== Модули курса =====================
class Module(db.Model):
    __tablename__ = 'modules'

    id_module = db.Column(db.Integer, primary_key=True)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))
    order_index = db.Column(db.Integer)
    video_link = db.Column(db.String(255))

    course = db.relationship('Course', back_populates='modules')
    materials = db.relationship('Material', back_populates='module')
    practice_stages = db.relationship('PracticeStage', back_populates='module')
    tests = db.relationship('Test', back_populates='module')

    def __repr__(self):
        return f"<Module {self.title}>"


# ===================== Материалы =====================
class Material(db.Model):
    __tablename__ = 'materials'

    id_material = db.Column(db.Integer, primary_key=True)
    id_module = db.Column(db.Integer, db.ForeignKey('modules.id_module'))
    file_name = db.Column(db.String(255))
    file_link = db.Column(db.String(255))

    module = db.relationship('Module', back_populates='materials')


# ===================== Практические этапы =====================
class PracticeStage(db.Model):
    __tablename__ = 'practice_stages'

    id_stage = db.Column(db.Integer, primary_key=True)
    id_module = db.Column(db.Integer, db.ForeignKey('modules.id_module'))
    step_number = db.Column(db.Integer)
    step_description = db.Column(db.Text)
    image = db.Column(db.String(255))

    module = db.relationship('Module', back_populates='practice_stages')


# ===================== Тесты =====================
class Test(db.Model):
    __tablename__ = 'tests'

    id_test = db.Column(db.Integer, primary_key=True)
    id_module = db.Column(db.Integer, db.ForeignKey('modules.id_module'))
    title = db.Column(db.String(255))
    passing_score = db.Column(db.Integer)

    module = db.relationship('Module', back_populates='tests')
    questions = db.relationship('Question', back_populates='test')



class Question(db.Model):
    __tablename__ = 'questions'

    id_question = db.Column(db.Integer, primary_key=True)
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id_test'))
    question_text = db.Column(db.Text, nullable=False)

    test = db.relationship('Test', back_populates='questions')
    answers = db.relationship('Answer', back_populates='question')


class Answer(db.Model):
    __tablename__ = 'answers'

    id_answer = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer, db.ForeignKey('questions.id_question'))
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    question = db.relationship('Question', back_populates='answers')


# ===================== Отзывы =====================
class Review(db.Model):
    __tablename__ = 'reviews'

    id_review = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    comment = db.Column(db.Text)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='reviews')
    course = db.relationship('Course', back_populates='reviews')


# ===================== Прогресс =====================
class Progress(db.Model):
    __tablename__ = 'progress'

    id_progress = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    is_completed = db.Column(db.Boolean)
    completed_modules = db.Column(db.Integer)
    completion_date = db.Column(db.DateTime)
    completed_modules_ids = db.Column(MutableList.as_mutable(JSON), default=[])
    user = db.relationship('User', back_populates='progress')
    course = db.relationship('Course', back_populates='progress')


# ===================== Покупки =====================
from datetime import datetime

class Purchase(db.Model):
    __tablename__ = 'purchases'
    id_purchase = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(
        db.Integer,
        db.ForeignKey('users.id_user'),
        nullable=False
    )
    id_course = db.Column(
        db.Integer,
        db.ForeignKey('courses.id_course'),
        nullable=False
    )
    price_byn = db.Column(
        db.Integer,
        nullable=False
    )
    status = db.Column(
        db.String(20),
        nullable=False,
        default='pending'
    )
    stripe_session_id = db.Column(
        db.String(255),
        unique=True,
        nullable=True
    )
    payment_link = db.Column(db.Text)
    purchase_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    user = db.relationship('User', back_populates='purchases')
    course = db.relationship('Course', back_populates='purchases')



# ===================== Сертификаты =====================
class Certificate(db.Model):
    __tablename__ = 'certificates'

    id_certificate = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(255))

    user = db.relationship('User', back_populates='certificates')
    course = db.relationship('Course', back_populates='certificates')


# ===================== Детали курса =====================
class CourseDetail(db.Model):
    __tablename__ = 'course_details'

    id_details = db.Column(db.Integer, primary_key=True)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))
    full_description = db.Column(db.Text)
    learning_outcomes = db.Column(db.Text)
    requirements = db.Column(db.Text)

    course = db.relationship('Course', back_populates='details')
