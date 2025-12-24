from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import User, Course, Purchase, Progress, Certificate, Module
from app.utils.certificate_generator import generate_certificate_image  # новый генератор через PIL
from datetime import datetime

profile_bp = Blueprint('profile', __name__, template_folder='../templates')

UPLOAD_FOLDER = 'app/static/uploads/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/profile/update', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(success=False, message="Не авторизован"), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify(success=False, message="Пользователь не найден"), 404

    # текстовые поля
    user.first_name = request.form.get('first_name', user.first_name)
    user.email = request.form.get('email', user.email)

    avatar_url = None
    file = request.files.get('avatar')
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"user_{user.id_user}.{ext}")
        path = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file.save(path)
        user.avatar = f'uploads/avatars/{filename}'
        avatar_url = url_for('static', filename=user.avatar)

    db.session.commit()
    return jsonify(success=True, avatar_url=avatar_url), 200


@profile_bp.route('/certificate/<int:course_id>')
def download_certificate(course_id):
    user_id = session.get('user_id')
    cert = Certificate.query.filter_by(
        id_user=user_id,
        id_course=course_id
    ).first_or_404()
    return redirect(url_for('static', filename=cert.file_path))


@profile_bp.route('/profile')
def profile_page():
    user_id = session.get('user_id')
    if not user_id:
        flash("Пожалуйста, войдите в систему", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if not user:
        flash("Пользователь не найден", "error")
        return redirect(url_for('auth.login'))

    # Подготовка курсов
    courses_data = []
    completed_courses_count = 0

    for purchase in user.purchases:
        course = purchase.course
        if not course:
            continue

        # Прогресс пользователя
        progress = Progress.query.filter_by(
            id_user=user.id_user,
            id_course=course.id_course
        ).first()

        modules = Module.query.filter_by(id_course=course.id_course).order_by(Module.order_index).all()
        total_modules = len(modules)
        completed_modules_count = len(progress.completed_modules_ids) if progress else 0
        progress_percent = int((completed_modules_count / total_modules) * 100) if total_modules else 0

        # Курс считается завершённым только если все модули пройдены
        is_course_completed = progress and completed_modules_count == total_modules

        # Обновляем статус покупки
        if is_course_completed and purchase.status != 'completed':
            purchase.status = 'completed'
            db.session.commit()

        # Имя преподавателя
        teacher_name = f"{course.teacher.first_name} {course.teacher.last_name}" if course.teacher else "Имя Фамилия"

        courses_data.append({
            "id": course.id_course,
            "title": course.title,
            "short_description": course.short_description,
            "image": course.image or "img/default_course.png",
            "difficulty": course.difficulty,
            "status": purchase.status,
            "completed_modules": completed_modules_count,
            "total_modules": total_modules,
            "progress": progress_percent,
            "teacher": teacher_name,
            "purchase_date": purchase.purchase_date
        })

        if is_course_completed:
            completed_courses_count += 1

    # Подготовка сертификатов
    certificates_data = []
    certificates = Certificate.query.filter_by(id_user=user.id_user).all()
    for cert in certificates:
        course = Course.query.get(cert.id_course)
        teacher_name = f"{course.teacher.first_name} {course.teacher.last_name}" if course.teacher else "Имя Фамилия"
        certificates_data.append({
            "id_course": course.id_course,
            "title": course.title,
            "teacher": teacher_name,
            "issued_date": cert.issued_date,
            "file_path": cert.file_path
        })

    stats = {
        "courses": len(user.purchases),
        "completed": completed_courses_count,
        "certificates": len(certificates_data)
    }

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        courses=courses_data,
        certificates=certificates_data
    )
