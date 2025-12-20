from flask import Blueprint, render_template, session, redirect, url_for, current_app, flash
from app import db
from sqlalchemy import text

profile_bp = Blueprint('profile', __name__, template_folder='../templates')


@profile_bp.route('/profile')
def profile_page():
    user_id = session.get('user_id')
    current_app.logger.debug(f"[PROFILE] user_id в сессии: {user_id}")

    if not user_id:
        flash("Пожалуйста, войдите в систему", "warning")
        return redirect(url_for('auth.login'))

    # Получаем данные пользователя
    user = None
    stats = {"courses": 0, "completed": 0, "certificates": 0}

    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("CALL GetUserProfile(:user_id)"), {"user_id": user_id})
            user_row = result.mappings().first()
            current_app.logger.debug(f"[PROFILE] user_row: {user_row}")

            if not user_row:
                flash("Пользователь не найден", "error")
                return redirect(url_for('auth.login'))

            user = dict(user_row)

    except Exception as e:
        current_app.logger.error(f"[PROFILE] Ошибка при вызове GetUserProfile: {e}")
        flash("Ошибка загрузки профиля", "error")
        return redirect(url_for('auth.login'))

    # Получаем статистику пользователя (не критично, ошибки игнорируем)
    try:
        with db.engine.connect() as conn:
            res = conn.execute(text("CALL get_user_stats(:user_id)"), {"user_id": user_id})
            stats_row = res.fetchone()
            if stats_row:
                stats = {
                    "courses": stats_row[0] or 0,
                    "completed": stats_row[1] or 0,
                    "certificates": stats_row[2] or 0
                }
        current_app.logger.debug(f"[PROFILE] stats: {stats}")
    except Exception as e:
        current_app.logger.debug(f"[PROFILE] get_user_stats вызвал ошибку (игнорируется): {e}")

    return render_template('profile.html', user=user, stats=stats)
