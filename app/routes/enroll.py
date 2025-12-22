from flask import Blueprint, render_template

enroll_bp = Blueprint(
    'enroll',
    __name__,
    template_folder='../templates'
)

@enroll_bp.route('/enroll')
def enroll_page():
    return render_template('enroll.html')
