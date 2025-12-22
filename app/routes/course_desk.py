from flask import Blueprint, render_template
from sqlalchemy.sql import func
from app import db
from app.models import Course, Teacher, Review, Module

course_desk_bp = Blueprint(
    'course_desk',
    __name__,
    template_folder='../templates'
)

@course_desk_bp.route('/course/<int:id_course>')
def course_page(id_course):
    course = Course.query.get_or_404(id_course)
    teacher = course.teacher

    avg_rating = (
        db.session.query(func.avg(Review.rating))
        .filter(Review.id_course == id_course)
        .scalar()
    )
    avg_rating = round(float(avg_rating), 1) if avg_rating else 0

    reviews_count = Review.query.filter_by(id_course=id_course).count()
    video_count = Module.query.filter_by(id_course=id_course, type='theory').count()

    discount_percent = 25
    old_price = course.price + 200 if discount_percent else None

    student_count = course.students.count() if hasattr(course, 'students') else 0

    return render_template(
        'course_details.html',
        course=course,
        teacher=teacher,
        avg_rating=avg_rating,
        reviews_count=reviews_count,
        video_count=video_count,
        discount_percent=discount_percent,
        old_price=old_price,
        student_count=student_count,
        reviews=course.reviews  # передаём все отзывы для вкладки
    )
