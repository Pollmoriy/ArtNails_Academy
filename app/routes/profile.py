from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import User, Progress

profile_bp = Blueprint('profile', __name__, template_folder='../templates')


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

        # все модули курса
        total_modules = len(course.modules)

        # пройденные модули пользователя по этому курсу
        completed_modules = Progress.query.filter_by(
            id_user=user.id_user,
            id_course=course.id_course,
            is_completed=True
        ).count()

        progress = int((completed_modules / total_modules) * 100) if total_modules else 0

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
            "teacher": course.teacher,
            "purchase_date": purchase.purchase_date
        })

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        courses=courses
    )
