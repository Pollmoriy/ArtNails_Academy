from flask import Blueprint, render_template
from sqlalchemy.sql import func

from app import db
from app.models import (
    Course,
    Teacher,
    Review,
    Module
)

# 🔹 Blueprint
course_desk_bp = Blueprint(
    'course_desk',
    __name__,
    template_folder='../templates'
)


@course_desk_bp.route('/course/<int:id_course>')
def course_page(id_course):
    # 🎓 Курс
    course = Course.query.get_or_404(id_course)

    # 👩‍🏫 Преподаватель (через relationship)
    teacher = course.teacher

    # ⭐ Средний рейтинг
    avg_rating = (
        db.session.query(func.avg(Review.rating))
        .filter(Review.id_course == id_course)
        .scalar()
    )
    avg_rating = round(float(avg_rating), 1) if avg_rating else 0

    # 📝 Количество отзывов
    reviews_count = Review.query.filter_by(id_course=id_course).count()

    # 🎥 Количество видеоуроков (теория)
    video_count = Module.query.filter_by(
        id_course=id_course,
        type='theory'
    ).count()

    # 💸 СКИДКА (пока временная логика)
    discount_percent = 25  # можно потом вынести в БД
    old_price = None

    if discount_percent:
        old_price = course.price + 200

    return render_template(
        'course_details.html',
        course=course,
        teacher=teacher,
        avg_rating=avg_rating,
        reviews_count=reviews_count,
        video_count=video_count,
        discount_percent=discount_percent,
        old_price=old_price
    )
