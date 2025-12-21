from flask import Blueprint, render_template, abort
from sqlalchemy import func

from app import db
from app.models import Course, Teacher, Review, Module

# ❗ имя blueprint = course_desk
course_desk_bp = Blueprint(
    'course_desk',
    __name__,
    template_folder='../templates'
)


@course_desk_bp.route('/course/<int:id_course>')
def course_page(id_course):
    # курс + преподаватель
    course = (
        db.session.query(Course)
        .join(Teacher)
        .filter(Course.id_course == id_course)
        .first()
    )

    if not course:
        abort(404)

    # рейтинг и количество отзывов
    rating_data = (
        db.session.query(
            func.avg(Review.rating),
            func.count(Review.id_review)
        )
        .filter(Review.id_course == id_course)
        .first()
    )

    avg_rating = round(rating_data[0], 1) if rating_data[0] else 0
    reviews_count = rating_data[1]

    # количество видео (модули с видео)
    videos_count = (
        db.session.query(Module)
        .filter(
            Module.id_course == id_course,
            Module.video_link.isnot(None)
        )
        .count()
    )

    return render_template(
        'course_details.html',
        course=course,
        teacher=course.teacher,
        avg_rating=avg_rating,
        reviews_count=reviews_count,
        videos_count=videos_count
    )
