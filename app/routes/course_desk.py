from flask import Blueprint, render_template, abort
from app import db
from sqlalchemy import text

course_bp = Blueprint(
    'course',                 # ← ВАЖНО: это имя для url_for
    __name__,
    url_prefix=''              # без префикса, будет /course/1
)


@course_bp.route('/course/<int:id_course>')
def course_page(id_course):
    """
    Страница подробностей курса
    """

    # 1️⃣ Основная информация о курсе
    course_query = text("""
        SELECT 
            c.id_course,
            c.title,
            c.short_description,
            c.image,
            c.price,
            c.duration_weeks,
            c.difficulty
        FROM courses c
        WHERE c.id_course = :id_course
    """)

    course = db.session.execute(
        course_query,
        {"id_course": id_course}
    ).mappings().first()

    if not course:
        abort(404)

    # 2️⃣ Количество видео (модули с video_link)
    video_count_query = text("""
        SELECT COUNT(*) AS video_count
        FROM modules
        WHERE id_course = :id_course
          AND video_link IS NOT NULL
    """)

    video_count = db.session.execute(
        video_count_query,
        {"id_course": id_course}
    ).scalar()

    # 3️⃣ (пока заглушки — потом легко подключим)
    rating = 4.5
    reviews_count = 26
    teacher = {
        "name": "Анна Иванова",
        "position": "Ведущий преподаватель",
        "avatar": "images/teacher.jpg"
    }

    return render_template(
        'course_detail.html',
        course=course,
        video_count=video_count,
        rating=rating,
        reviews_count=reviews_count,
        teacher=teacher
    )
