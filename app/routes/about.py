from flask import Blueprint, render_template
from app.models import Teacher
from app import db

about_bp = Blueprint('about', __name__)


@about_bp.route("/about")
def about():
    teachers = Teacher.query.all()
    return render_template("about.html", teachers=teachers)
