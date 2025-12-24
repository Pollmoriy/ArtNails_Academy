from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import Course, Module, Material, PracticeStage, Test, Progress
from app import db
from flask import send_from_directory, send_file, abort, current_app
from werkzeug.utils import safe_join
import os
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


# Blueprint для страниц курса
course_bp = Blueprint('course', __name__, template_folder='../templates')

@course_bp.route('/course/<int:course_id>/complete_module/<int:module_id>', methods=['POST'])
def complete_module(course_id, module_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Пользователь не авторизован"}), 403

    # Получаем прогресс пользователя по курсу
    progress = Progress.query.filter_by(id_user=user_id, id_course=course_id).first()

    if not progress:
        # Если прогресса нет — создаём новый
        progress = Progress(
            id_user=user_id,
            id_course=course_id,
            completed_modules=0,
            completed_modules_ids=[]
        )
        db.session.add(progress)
        db.session.commit()  # сначала создаём, чтобы был id

    # Добавляем модуль в список завершённых, если ещё нет
    if module_id not in progress.completed_modules_ids:
        progress.completed_modules_ids.append(module_id)
        progress.completed_modules = len(progress.completed_modules_ids)

        # Если все модули пройдены, отмечаем курс как завершённый
        # total_modules нужно передавать из фронта или получать через модель Course/Module
        # Например:
        # total_modules = Module.query.filter_by(id_course=course_id).count()
        # if progress.completed_modules >= total_modules:
        #     progress.is_completed = True
        progress.completion_date = datetime.utcnow()

        db.session.commit()

    return jsonify({
        "success": True,
        "completed_modules": progress.completed_modules,
        "completed_modules_ids": progress.completed_modules_ids
    })

@course_bp.route('/download/<path:file_path>')
def download_file(file_path):
    full_path = os.path.join(current_app.static_folder, file_path)
    if os.path.exists(full_path):
        return send_file(full_path, as_attachment=True)
    return "Файл не найден", 404

@course_bp.route('/course/<int:course_id>')
def course_page(course_id):
    user_id = session.get('user_id')
    course = Course.query.get(course_id)
    if not course:
        flash("Курс не найден", "error")
        return redirect(url_for('profile.profile_page'))

    progress = None
    if user_id:
        progress = Progress.query.filter_by(id_user=user_id, id_course=course_id).first()

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

        if module.type == "theory":
            module_dict["materials"] = [
                {"id": m.id_material, "file_name": m.file_name, "file_link": m.file_link}
                for m in module.materials
            ]

        if module.type == "practice":
            module_dict["practice_stages"] = [
                {"step_number": ps.step_number, "step_description": ps.step_description, "image": ps.image}
                for ps in module.practice_stages
            ]

        if module.type == "test":
            module_dict["tests"] = []
            for t in module.tests:
                test_dict = {
                    "id_test": t.id_test,
                    "title": t.title,
                    "passing_score": t.passing_score,
                    "questions": [
                        {
                            "id_question": q.id_question,
                            "text": q.question_text,
                            "answers": [
                                {"id_answer": a.id_answer, "text": a.answer_text, "is_correct": a.is_correct}
                                for a in q.answers
                            ]
                        }
                        for q in t.questions
                    ]
                }
                module_dict["tests"].append(test_dict)

        modules_data.append(module_dict)

    # Получаем реальные ID завершённых модулей из БД
    completed_modules_ids = []
    if progress:
        if isinstance(progress.completed_modules_ids, str):
            completed_modules_ids = [int(mid) for mid in progress.completed_modules_ids.split(',') if mid]
        elif isinstance(progress.completed_modules_ids, list):
            completed_modules_ids = progress.completed_modules_ids

    completed_modules_count = len(completed_modules_ids)
    total_modules = len(modules)
    progress_percent = int((completed_modules_count / total_modules) * 100) if total_modules else 0

    # Определяем индекс последнего завершённого модуля
    last_completed_module_index = -1
    for i, module in enumerate(modules):
        if module.id_module in completed_modules_ids:
            last_completed_module_index = i

    return render_template(
        "course_page.html",
        course=course,
        modules=modules_data,
        progress_percent=progress_percent,
        completed_modules=completed_modules_count,
        completed_modules_ids=completed_modules_ids,
        total_modules=total_modules,
        last_completed_module_index=last_completed_module_index
    )

