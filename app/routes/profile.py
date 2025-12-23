from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import User, Progress
from flask import request
from werkzeug.utils import secure_filename
import os
from app import db

profile_bp = Blueprint('profile', __name__, template_folder='../templates')


UPLOAD_FOLDER = 'app/static/uploads/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route('/profile/update', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return '', 401

    user = User.query.get(user_id)
    if not user:
        return '', 404

    # текстовые поля
    user.first_name = request.form.get('first_name')
    user.email = request.form.get('email')
    user.phone = request.form.get('phone')

    # аватар
    file = request.files.get('avatar')
    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{user.id_user}.{file.filename.rsplit('.',1)[1]}")
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        user.avatar = f'uploads/avatars/{filename}'

    db.session.commit()
    return '', 200

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

    # -------------------------
    # Статистика пользователя
    # -------------------------
    stats = {
        "courses": len(user.purchases),
        "completed": sum(1 for p in user.purchases if p.status == 'completed'),
        "certificates": len(user.certificates)
    }

    # -------------------------
    # Курсы пользователя
    # -------------------------
    courses = []

    for purchase in user.purchases:
        course = purchase.course
        if not course:
            continue

        total_modules = len(course.modules)

        # ----------------------------
        # Считаем завершённые модули по этому курсу
        # Если Progress хранит is_completed для всего курса, а не для модуля
        completed_modules = total_modules if purchase.status == 'completed' else 0

        progress = int((completed_modules / total_modules) * 100) if total_modules else 0

        # ФИО преподавателя сразу строкой
        teacher_name = (
            f"{course.teacher.first_name} {course.teacher.last_name}"
            if course.teacher else "Имя Фамилия"
        )

        courses.append({
            "id": course.id_course,
            "title": course.title,
            "short_description": course.short_description,
            "image": course.image or "img/default_course.png",
            "difficulty": course.difficulty,
            "status": purchase.status,
            "completed_modules": completed_modules,
            "total_modules": total_modules,
            "progress": progress,
            "teacher": teacher_name,
            "purchase_date": purchase.purchase_date
        })

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        courses=courses
    )
