from flask import Blueprint, render_template, request, jsonify
from app import db
from sqlalchemy import text

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/catalog')
def catalog():
    search = request.args.get('search', '')
    level = request.args.get('level') or None

    price = request.args.get('price')
    duration = request.args.get('duration')

    # ---- цена ----
    price_min, price_max = 0, 999999
    if price == 'low':
        price_max = 800
    elif price == 'medium':
        price_min, price_max = 801, 1200
    elif price == 'high':
        price_min = 1201

    # ---- длительность ----
    duration_min, duration_max = 0, 100
    if duration == 'short':
        duration_max = 2
    elif duration == 'medium':
        duration_min, duration_max = 3, 4
    elif duration == 'long':
        duration_min = 5

    sql = text("""
        CALL SearchCourses(
            :search,
            :level,
            :price_min,
            :price_max,
            :duration_min,
            :duration_max
        )
    """)

    params = {
        "search": search,
        "level": level,
        "price_min": price_min,
        "price_max": price_max,
        "duration_min": duration_min,
        "duration_max": duration_max
    }

    with db.engine.connect() as conn:
        result = conn.execute(sql, params)
        courses = [dict(row) for row in result.mappings()]

    # AJAX-запрос
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(courses)

    return render_template("catalog.html", courses=courses)
