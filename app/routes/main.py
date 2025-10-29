from flask import Blueprint, render_template, session
from app.models import User


main_bp = Blueprint(
    'main',
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

@main_bp.route('/')
def home():
    popular_courses = [
        {
            "image": "img/IMAGE.png",
            "level": "Начальный",
            "weeks": 3,
            "title": "Мастер маникюра",
            "description": "Изучите основы классического и европейского маникюра. Курс включает теорию анатомии ногтей, правила гигиены, работу с инструментами и базовые техники.",
            "price": "1500 BYN"
        },
        {
            "image": "img/IMAGE.png",
            "level": "Продвинутый",
            "weeks": 4,
            "title": "Дизайн ногтей",
            "description": "Полный курс по работе с гель-лаками: подготовка ногтей, техники нанесения, создание градиентов, френча и других популярных покрытий.",
            "price": "1800 BYN"
        },
        {
            "image": "img/IMAGE.png",
            "level": "Начальный",
            "weeks": 2,
            "title": "Маникюр для себя",
            "description": "Освойте сложные техники дизайна: роспись, стемпинг, объемный декор, работа с фольгой и стразами. Создавайте уникальные авторские дизайны.",
            "price": "1200 BYN"
        }
    ]
    return render_template('home.html', popular_courses=popular_courses)


