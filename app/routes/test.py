from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import Test, Question, Answer
from app import db

test_bp = Blueprint('test', __name__, template_folder='../templates')

@test_bp.route('/test/<int:test_id>')
def test_page(test_id):
    # Получаем тест
    test = Test.query.get(test_id)
    if not test:
        flash("Тест не найден", "error")
        return redirect(url_for('course.course_page', course_id=1))  # или другую страницу

    # Получаем вопросы и ответы
    questions_data = []
    for q in test.questions:
        questions_data.append({
            "id": q.id_question,
            "text": q.question_text,
            "answers": [{"id": a.id_answer, "text": a.answer_text, "is_correct": a.is_correct} for a in q.answers]
        })

    return render_template('test_page.html', test=test, questions=questions_data)
