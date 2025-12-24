import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from app import db
from app.models import Certificate

CERT_FOLDER = 'app/static/certificates'

def generate_certificate(user, course):
    os.makedirs(CERT_FOLDER, exist_ok=True)

    filename = f"certificate_user_{user.id_user}_course_{course.id_course}.pdf"
    file_path = os.path.join(CERT_FOLDER, filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # ===== ШАБЛОН =====
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 150, "СЕРТИФИКАТ")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 220, "Настоящим подтверждается, что")

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(
        width / 2,
        height - 270,
        f"{user.first_name} {user.last_name}"
    )

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 320, "успешно прошёл(а) курс")

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 360, course.title)

    issue_date = datetime.utcnow().strftime('%d.%m.%Y')
    c.setFont("Helvetica", 12)
    c.drawString(50, 100, f"Дата выдачи: {issue_date}")

    c.showPage()
    c.save()

    # ===== СОХРАНЕНИЕ В БД =====
    certificate = Certificate(
        id_user=user.id_user,
        id_course=course.id_course,
        file_path=f"certificates/{filename}"
    )

    db.session.add(certificate)
    db.session.commit()

    return certificate
