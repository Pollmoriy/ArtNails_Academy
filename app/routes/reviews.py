from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
from app import db
from app.models import Review, Course, User, Purchase

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route('/reviews')
def reviews_page():
    course_id = request.args.get('course', type=int)
    sort = request.args.get('sort', 'newest')

    query = Review.query.join(User).join(Course)

    if course_id:
        query = query.filter(Review.id_course == course_id)

    if sort == 'newest':
        query = query.order_by(Review.created_at.desc())
    elif sort == 'oldest':
        query = query.order_by(Review.created_at.asc())
    elif sort == 'rating':
        query = query.order_by(Review.rating.desc())

    reviews = query.all()

    # ===== AJAX =====
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        current_user_id = session.get('user_id')

        return jsonify([
            {
                'id': r.id_review,
                'user_name': f'{r.user.first_name} {r.user.last_name}',
                'course_title': r.course.title,
                'rating': r.rating,
                'comment': r.comment,
                'created_at': r.created_at.strftime('%d.%m.%Y'),
                'avatar': r.user.avatar,
                'is_owner': session.get('user_id') == r.id_user
            }
            for r in reviews
        ])

    # ===== обычная загрузка =====
    courses = Course.query.all()

    user_courses = []
    if session.get('user_id'):
        user_courses = [
            p.course for p in
            Purchase.query.filter_by(id_user=session['user_id']).all()
        ]

    return render_template(
        'reviews.html',
        reviews=reviews,
        courses=courses,
        user_courses=user_courses
    )


@reviews_bp.route('/reviews/add', methods=['POST'])
def add_review():
    if not session.get('user_id'):
        return jsonify({'success': False, 'error': 'Не авторизованы'})

    data = request.get_json()
    course_id = int(data.get('course_id'))
    rating = int(data.get('rating'))
    comment = data.get('comment')

    purchased = Purchase.query.filter_by(
        id_user=session['user_id'],
        id_course=course_id
    ).first()

    if not purchased:
        return jsonify({'success': False, 'error': 'Курс не куплен'})

    review = Review(
        id_user=session['user_id'],
        id_course=course_id,
        rating=rating,
        comment=comment,
        created_at=datetime.utcnow()
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({'success': True})


@reviews_bp.route('/reviews/delete', methods=['POST'])
def delete_review():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'Не авторизованы'})

    data = request.get_json()
    review_id = data.get('review_id')

    review = Review.query.get(review_id)
    if not review:
        return jsonify({'success': False, 'error': 'Отзыв не найден'})

    if review.id_user != user_id:
        return jsonify({'success': False, 'error': 'Нет прав'})

    db.session.delete(review)
    db.session.commit()

    return jsonify({'success': True})
