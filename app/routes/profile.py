from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.models import User, Progress
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

        # Получаем прогресс пользователя по этому курсу
        progress = Progress.query.filter_by(id_user=user.id_user, id_course=course.id_course).first()
        completed_modules_ids = progress.completed_modules_ids if progress else []

        # Сортируем модули по порядку
        modules = sorted(course.modules, key=lambda m: m.order_index)
        total_modules = len(modules)

        # Считаем завершённые модули, учитывая доступность тестов
        completed_count = 0
        for i, module in enumerate(modules):
            if module.id_module in completed_modules_ids:
                completed_count += 1
            elif module.type == 'test':
                # Проверка для тестов по правилам:
                # 1-й тест: модули 1–6 должны быть пройдены
                # 2-й тест: модули 1–8
                # финальный: модули 1–11
                if module.id_module == 7:
                    required = [1,2,3,4,5,6]
                elif module.id_module == 9:
                    required = [1,2,3,4,5,6,7,8]
                elif module.id_module == 12:
                    required = [1,2,3,4,5,6,7,8,9,10,11]
                else:
                    required = []

                if required and all(r in completed_modules_ids for r in required):
                    completed_count += 1  # тест доступен, учитываем

        progress_percent = int((completed_count / total_modules) * 100) if total_modules else 0

        teacher_name = (
            f"{course.teacher.first_name} {course.teacher.last_name}" if course.teacher else "Имя Фамилия"
        )

        courses.append({
            "id": course.id_course,
            "title": course.title,
            "short_description": course.short_description,
            "image": course.image or "img/default_course.png",
            "difficulty": course.difficulty,
            "status": purchase.status,
            "completed_modules": completed_count,
            "total_modules": total_modules,
            "progress": progress_percent,
            "teacher": teacher_name,
            "purchase_date": purchase.purchase_date
        })

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        courses=courses
    )
