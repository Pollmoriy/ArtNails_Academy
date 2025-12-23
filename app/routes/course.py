from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import Course, Module, Material, PracticeStage, Test, Progress
from app import db

# Blueprint для страниц курса
course_bp = Blueprint('course', __name__, template_folder='../templates')

@course_bp.route('/course/<int:course_id>')
def course_page(course_id):
    # Получаем текущего пользователя
    user_id = session.get('user_id')

    # Получаем курс
    course = Course.query.get(course_id)
    if not course:
        flash("Курс не найден", "error")
        return redirect(url_for('profile.profile_page'))

    # Получаем прогресс пользователя по курсу, если авторизован
    progress = None
    if user_id:
        progress = Progress.query.filter_by(id_user=user_id, id_course=course_id).first()

    # Получаем модули курса, упорядоченные по порядковому индексу
    modules = Module.query.filter_by(id_course=course_id).order_by(Module.order_index).all()
    modules_data = []

    for module in modules:
        module_dict = {
            "id": module.id_module,
            "title": module.title,
            "type": module.type,
            "description": module.description,
            "video_link": module.video_link,
            "materials": [],
            "practice_stages": [],
            "tests": []
        }

        # Добавляем материалы для теоретических модулей
        if module.type == "theory":
            module_dict["materials"] = [
                {
                    "id": m.id_material,
                    "file_name": m.file_name,
                    "file_link": m.file_link
                } for m in module.materials
            ]

        # Добавляем шаги для практических модулей
        if module.type == "practice":
            module_dict["practice_stages"] = [
                {
                    "step_number": ps.step_number,
                    "step_description": ps.step_description,
                    "image": ps.image
                } for ps in module.practice_stages
            ]

        # Добавляем тесты для модулей типа "test"
        if module.type == "test":
            module_dict["tests"] = [
                {
                    "id_test": t.id_test,
                    "title": t.title
                } for t in module.tests
            ]

        modules_data.append(module_dict)

    # Вычисляем список id завершённых модулей
    completed_modules_count = progress.completed_modules if progress else 0
    completed_modules_ids = [module.id_module for module in modules[:completed_modules_count]] if modules else []

    # Общее количество модулей
    total_modules = len(modules)

    # Процент завершения
    completed_count = len(completed_modules_ids)
    progress_percent = int((completed_count / total_modules) * 100) if total_modules else 0

    # Рендерим страницу курса
    return render_template(
        "course_page.html",  # убедись, что файл лежит в app/templates/
        course=course,
        modules=modules_data,
        progress_percent=progress_percent,
        completed_modules=completed_count,
        completed_modules_ids=completed_modules_ids,
        total_modules=total_modules
    )
