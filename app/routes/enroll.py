from flask import Blueprint, render_template, request, redirect, flash
from app.models import Course

enroll_bp = Blueprint(
    'enroll',
    __name__,
    template_folder='../templates'
)

@enroll_bp.route('/enroll', methods=['GET', 'POST'])
def enroll():
    courses = Course.query.all()

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        course_id = request.form.get('course')
        payment = request.form.get('payment')
        agree = request.form.get('agree')

        errors = []

        if len(full_name) < 3:
            errors.append('Некорректное имя')

        if '@' not in email:
            errors.append('Некорректный email')

        if len(phone) < 7:
            errors.append('Некорректный телефон')

        if not course_id:
            errors.append('Курс не выбран')

        if not payment:
            errors.append('Не выбран способ оплаты')

        if not agree:
            errors.append('Не принято соглашение')

        if errors:
            for err in errors:
                flash(err, 'error')
            return redirect('/enroll')

        # TODO: сохранение записи в БД
        flash('Вы успешно записались на курс!', 'success')
        return redirect('/')

    return render_template('enroll.html', courses=courses)
