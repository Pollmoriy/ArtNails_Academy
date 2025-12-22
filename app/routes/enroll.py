from flask import (
    Blueprint, render_template, request,
    jsonify, session, url_for, current_app
)
from app import db
from app.models import Course, Purchase
import stripe

enroll_bp = Blueprint('enroll', __name__, url_prefix='/enroll')

EUR_RATE = 0.30  # временно, конвертация BYN -> EUR

# ---------- СТРАНИЦА ЗАПИСИ НА КУРС ----------
@enroll_bp.route('/', methods=['GET'])
def enroll_page():
    courses = Course.query.all()
    return render_template(
        'enroll.html',
        courses=courses,
        stripe_public_key=current_app.config['STRIPE_PUBLISHABLE_KEY']
    )

# ---------- СОЗДАНИЕ STRIPE SESSION ----------
@enroll_bp.route('/create-stripe-session', methods=['POST'])
def create_stripe_session():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    course_id = data.get('course_id')

    course = Course.query.get_or_404(course_id)

    # Цена в BYN
    price_byn = float(course.price)

    # Конвертация в EUR (Stripe принимает цену в центах)
    price_eur = int(price_byn * EUR_RATE * 100)

    # 1️⃣ Создаем запись о покупке (pending)
    purchase = Purchase(
        id_user=session['user_id'],
        id_course=course.id_course,
        price_byn=price_byn,
        status='pending'
    )
    db.session.add(purchase)
    db.session.commit()

    # 2️⃣ Создаем Stripe Checkout Session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': course.title},
                    'unit_amount': price_eur,
                },
                'quantity': 1,
            }],
            success_url=url_for("main.home", _external=True) + "?payment=success",
            cancel_url=url_for("main.home", _external=True) + "?payment=cancel"
        )
    except stripe.error.StripeError as e:
        # Ошибка при создании платежа
        return jsonify({'error': str(e)}), 500

    # 3️⃣ Сохраняем Stripe session и ссылку
    purchase.stripe_session_id = checkout_session.id
    purchase.payment_link = checkout_session.url
    db.session.commit()

    return jsonify({'url': checkout_session.url})
