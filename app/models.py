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

    # связи
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    purchases = db.relationship('Purchase', back_populates='user', cascade="all, delete-orphan")
    progress = db.relationship('Progress', back_populates='user', cascade="all, delete-orphan")
    certificates = db.relationship('Certificate', back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


# 🎓 Курсы
class Course(db.Model):
    __tablename__ = 'courses'

    id_course = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2), default=0.00)

    # связи
    modules = db.relationship('Module', back_populates='course', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='course', cascade="all, delete-orphan")
    purchases = db.relationship('Purchase', back_populates='course', cascade="all, delete-orphan")
    certificates = db.relationship('Certificate', back_populates='course', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course {self.title}>"


# 📘 Модули
class Module(db.Model):
    __tablename__ = 'modules'

    id_module = db.Column(db.Integer, primary_key=True)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    # связи
    course = db.relationship('Course', back_populates='modules')
    tests = db.relationship('Test', back_populates='module', cascade="all, delete-orphan")
    progress = db.relationship('Progress', back_populates='module', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Module {self.title}>"


# 🧾 Тесты
class Test(db.Model):
    __tablename__ = 'tests'

    id_test = db.Column(db.Integer, primary_key=True)
    id_module = db.Column(db.Integer, db.ForeignKey('modules.id_module'), nullable=False)
    title = db.Column(db.String(255))

    module = db.relationship('Module', back_populates='tests')
    questions = db.relationship('Question', back_populates='test', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Test {self.title}>"


# ❓ Вопросы
class Question(db.Model):
    __tablename__ = 'questions'

    id_question = db.Column(db.Integer, primary_key=True)
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id_test'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)

    test = db.relationship('Test', back_populates='questions')
    answers = db.relationship('Answer', back_populates='question', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Question {self.id_question}>"


# ✅ Ответы
class Answer(db.Model):
    __tablename__ = 'answers'

    id_answer = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer, db.ForeignKey('questions.id_question'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    question = db.relationship('Question', back_populates='answers')

    def __repr__(self):
        return f"<Answer {self.id_answer}>"


# 💰 Покупки
class Purchase(db.Model):
    __tablename__ = 'purchases'

    id_purchase = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='purchases')
    course = db.relationship('Course', back_populates='purchases')

    def __repr__(self):
        return f"<Purchase {self.id_purchase}>"


# 💬 Отзывы
class Review(db.Model):
    __tablename__ = 'reviews'

    id_review = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'), nullable=False)
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='reviews')
    course = db.relationship('Course', back_populates='reviews')

    def __repr__(self):
        return f"<Review {self.id_review}>"


# 📊 Прогресс
class Progress(db.Model):
    __tablename__ = 'progress'

    id_progress = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    id_module = db.Column(db.Integer, db.ForeignKey('modules.id_module'), nullable=False)
    status = db.Column(db.Enum('not_started', 'in_progress', 'completed'), default='not_started')
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='progress')
    module = db.relationship('Module', back_populates='progress')

    def __repr__(self):
        return f"<Progress {self.id_progress}>"


# 🏅 Сертификаты
class Certificate(db.Model):
    __tablename__ = 'certificates'

    id_certificate = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'), nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    certificate_code = db.Column(db.String(64), unique=True)

    user = db.relationship('User', back_populates='certificates')
    course = db.relationship('Course', back_populates='certificates')

    def __repr__(self):
        return f"<Certificate {self.certificate_code}>"


# 👩‍🏫 Преподаватели
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id_teacher = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    photo = db.Column(db.String(255))

    def __repr__(self):
        return f"<Teacher {self.first_name} {self.last_name}>"
