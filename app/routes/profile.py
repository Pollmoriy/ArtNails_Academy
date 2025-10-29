from flask import Blueprint, render_template, session, redirect, url_for
from app import db
from app.models import User
from sqlalchemy import text

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def profile_page():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.login'))

    # Вызов процедуры с обёрткой text()
    result = db.session.execute(text("CALL get_user_stats(:uid)"), {'uid': user_id})
    stats_row = result.fetchone()
    stats = {
        'courses': stats_row[0] if stats_row else 0,
        'completed': stats_row[1] if stats_row else 0,
        'certificates': stats_row[2] if stats_row else 0
    }

    return render_template('profile.html', user=user, stats=stats)
