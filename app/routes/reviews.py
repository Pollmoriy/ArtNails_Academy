from flask import Blueprint, render_template, request, jsonify
from app.models import Review, Course, User

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/reviews')
def reviews_page():
    # Получаем параметры
    course_id = request.args.get('course', type=int)
    sort = request.args.get('sort', 'newest')  # newest, oldest, rating

    # Базовый запрос с джойнами
    query = Review.query.join(User).join(Course)

    # Фильтр по курсу
    if course_id:
        query = query.filter(Review.id_course == course_id)

    # Сортировка
    if sort == 'newest':
        query = query.order_by(Review.created_at.desc())
    elif sort == 'oldest':
        query = query.order_by(Review.created_at.asc())
    elif sort == 'rating':
        query = query.order_by(Review.rating.desc())

    reviews = query.all()

    # AJAX-запрос
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        reviews_data = []
        for r in reviews:
            reviews_data.append({
                'id': r.id_review,
                'user_name': f"{r.user.first_name} {r.user.last_name}",
                'course_title': r.course.title,
                'rating': r.rating,
                'comment': r.comment,
                'created_at': r.created_at.strftime('%d.%m.%Y'),
                'avatar': r.user.avatar
            })
        return jsonify(reviews_data)

    # Стандартная страница
    courses = Course.query.all()
    return render_template(
        "reviews.html",
        reviews=reviews,
        courses=courses,
        selected_course=course_id,
        selected_sort=sort
    )
