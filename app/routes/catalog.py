from flask import Blueprint, render_template, request, jsonify
from app import db
from sqlalchemy import text

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/catalog')
def catalog():
    search = request.args.get('search', '')
    level = request.args.get('level')
    if not level:
        level = None
    price_min = request.args.get('price_min', 0, type=float)
    price_max = request.args.get('price_max', 999999, type=float)
    duration_min = request.args.get('duration_min', 0, type=int)
    duration_max = request.args.get('duration_max', 100, type=int)

    # DEBUG: параметры перед SQL
    print("DEBUG: Параметры для SQL", {
        "search_term": search,
        "level_filter": level,
        "price_min": price_min,
        "price_max": price_max,
        "duration_min": duration_min,
        "duration_max": duration_max
    })

    sql = text("""
        CALL SearchCourses(:search_term, :level_filter, :price_min, :price_max, :duration_min, :duration_max)
    """)
    params = {
        "search_term": search,
        "level_filter": level,
        "price_min": price_min,
        "price_max": price_max,
        "duration_min": duration_min,
        "duration_max": duration_max
    }

    with db.engine.connect() as conn:
        result = conn.execute(sql, params)
        # Важно: используем .mappings() для преобразования в словари
        courses = [dict(row) for row in result.mappings()]

    # DEBUG: сколько курсов получено
    print("DEBUG: Получено курсов", len(courses))

    if request.args.get('ajax'):
        return jsonify(courses)

    return render_template("catalog.html", courses=courses)
