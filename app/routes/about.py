from flask import Blueprint, render_template
from app.models import Teacher
from app import db

# Создаём blueprint для страницы "О нас"
about_bp = Blueprint('about', __name__)


@about_bp.route("/about")
def about():
    # Получаем всех преподавателей из таблицы teachers
    teachers = Teacher.query.all()

    # Передаём данные в шаблон about.html
    return render_template("about.html", teachers=teachers)
