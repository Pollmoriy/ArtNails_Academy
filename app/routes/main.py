from flask import Blueprint, render_template
from sqlalchemy import text
from app import db

main_bp = Blueprint(
    'main',
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

@main_bp.route('/')
def home():
    # Получаем популярные курсы через хранимую процедуру
    with db.engine.connect() as conn:
        result = conn.execute(
            text("CALL GetPopularCourses(:limit)"),
            {"limit": 3}
        )
        popular_courses = result.mappings().all()

    return render_template(
        'home.html',
        popular_courses=popular_courses
    )
