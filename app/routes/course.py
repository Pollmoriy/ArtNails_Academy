from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import Course, Module, Material, PracticeStage, Test, Progress
from app import db
from flask import send_from_directory, send_file, abort, current_app
from werkzeug.utils import safe_join
import os

# Blueprint для страниц курса
course_bp = Blueprint('course', __name__, template_folder='../templates')

@course_bp.route('/download/<path:file_path>')
def download_file(file_path):
    full_path = os.path.join(current_app.static_folder, file_path)
    return send_file(full_path, as_attachment=True)

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

        # Теоретические материалы
        if module.type == "theory":
            module_dict["materials"] = [
                {
                    "id": m.id_material,
                    "file_name": m.file_name,
                    "file_link": m.file_link
                } for m in module.materials
            ]

        # Практические этапы
        if module.type == "practice":
            module_dict["practice_stages"] = [
                {
                    "step_number": ps.step_number,
                    "step_description": ps.step_description,
                    "image": ps.image
                } for ps in module.practice_stages
            ]

        # Тесты с вопросами и ответами
        if module.type == "test":
            module_dict["tests"] = []
            for t in module.tests:
                test_dict = {
                    "id_test": t.id_test,
                    "title": t.title,
                    "passing_score": t.passing_score,
                    "questions": []
                }
                for q in t.questions:  # вопросы привязаны к тесту
                    question_dict = {
                        "id_question": q.id_question,
                        "text": q.question_text,  # правильное поле
                        "answers": [
                            {
                                "id_answer": a.id_answer,
                                "text": a.answer_text,  # правильное поле
                                "is_correct": a.is_correct
                            }
                            for a in q.answers  # ответы привязаны к вопросу
                        ]
                    }
                    test_dict["questions"].append(question_dict)
                module_dict["tests"].append(test_dict)

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
        "course_page.html",
        course=course,
        modules=modules_data,
        progress_percent=progress_percent,
        completed_modules=completed_count,
        completed_modules_ids=completed_modules_ids,
        total_modules=total_modules
    )
