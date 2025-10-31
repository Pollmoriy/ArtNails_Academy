from flask import Blueprint, render_template, request
from app import db
from app.models import Course, Teacher

# Создаём blueprint
catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/catalog')
def catalog():
    """
    Страница каталога курсов.
    Пока просто выводим все курсы (логика фильтрации будет позже).
    """
    # Получаем все курсы из БД
    courses = Course.query.all()

    # Передаём в шаблон
    return render_template("catalog.html", courses=courses)
