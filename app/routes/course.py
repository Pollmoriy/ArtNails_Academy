from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import Course, Module, Material, PracticeStage, Test, Progress
from app import db
from flask import send_from_directory, send_file, abort, current_app
from werkzeug.utils import safe_join
import os
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError



# Blueprint для страниц курса
course_bp = Blueprint('course', __name__, template_folder='../templates')


@course_bp.route('/course/<int:course_id>/complete_module/<int:module_id>', methods=['POST'])
def complete_module(course_id, module_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "error": "Не авторизован"}), 401

    progress = Progress.query.filter_by(id_user=user_id, id_course=course_id).first()
    if not progress:
        # создаём запись, если её нет
        progress = Progress(
            id_user=user_id,
            id_course=course_id,
            completed_modules_ids=[]
        )
        db.session.add(progress)

    # Преобразуем JSON колонку в список
    completed_ids = progress.completed_modules_ids or []

    if module_id not in completed_ids:
        completed_ids.append(module_id)
        progress.completed_modules_ids = completed_ids
        progress.completed_modules = len(completed_ids)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({
        "success": True,
        "completed_modules": len(progress.completed_modules_ids)
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
        if progress is None:
            progress = Progress(id_user=user_id, id_course=course_id, completed_modules_ids=[])
            db.session.add(progress)
            db.session.commit()

    modules = Module.query.filter_by(id_course=course_id).order_by(Module.order_index).all()
    modules_data = []

    for module in modules:
        module_dict = {
            "id": module.id_module,
            "title": module.title,
            "type": module.type,
            "description": module.description,
            "video_link": module.video_link,
            "materials": [{"id": m.id_material, "file_name": m.file_name, "file_link": m.file_link} for m in getattr(module, "materials", [])],
            "practice_stages": [{"step_number": ps.step_number, "step_description": ps.step_description, "image": ps.image} for ps in getattr(module, "practice_stages", [])],
            "tests": []
        }

        if module.type == "test":
            for t in getattr(module, "tests", []):
                test_dict = {
                    "id_test": t.id_test,
                    "title": t.title,
                    "passing_score": t.passing_score,
                    "questions": [{"id_question": q.id_question, "text": q.question_text, "answers": [{"id_answer": a.id_answer, "text": a.answer_text, "is_correct": a.is_correct} for a in getattr(q, "answers", [])]} for q in getattr(t, "questions", [])]
                }
                module_dict["tests"].append(test_dict)

        modules_data.append(module_dict)

    completed_modules_ids = progress.completed_modules_ids or []
    completed_count = len(completed_modules_ids)
    total_modules = len(modules)
    progress_percent = int((completed_count / total_modules) * 100) if total_modules else 0

    return render_template(
        "course_page.html",
        course=course,
        modules=modules_data,
        completed_modules=completed_count,
        completed_modules_ids=completed_modules_ids,
        total_modules=total_modules,
        progress_percent=progress_percent
    )
