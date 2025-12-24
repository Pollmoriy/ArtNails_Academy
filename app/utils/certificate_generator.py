import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from app import db
from app.models import Certificate

# Пути к шрифтам
FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'fonts')
FONT_BOLD = os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf')
FONT_REGULAR = os.path.join(FONT_DIR, 'DejaVuSans.ttf')

# Папка для сертификатов
CERT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'certificates', 'generated')
os.makedirs(CERT_DIR, exist_ok=True)

def generate_certificate_image(user, course):
    """
    Генерация сертификата как изображения для завершённого курса
    """
    # Проверяем, есть ли уже сертификат
    existing_cert = Certificate.query.filter_by(
        id_user=user.id_user,
        id_course=course.id_course
    ).first()
    if existing_cert:
        return existing_cert.file_path

    # Размер сертификата
    width, height = 1123, 794
    background_color = (255, 255, 255)  # белый фон
    border_color = (202, 168, 92)  # золотистая рамка

    # Создаём изображение
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # ---------- РАМКА ----------
    border_width = 10
    draw.rectangle(
        [border_width//2, border_width//2, width-border_width//2, height-border_width//2],
        outline=border_color,
        width=border_width
    )

    # ---------- ТЕНЬ для текста ----------
    def draw_text_centered(text, y, font, fill=(0,0,0)):
        bbox = draw.textbbox((0,0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) / 2
        # Тень
        draw.text((x+2, y+2), text, font=font, fill=(150,150,150))
        # Сам текст
        draw.text((x, y), text, font=font, fill=fill)
        return text_height

    # Шрифты
    font_name = ImageFont.truetype(FONT_BOLD, 48)
    font_course = ImageFont.truetype(FONT_BOLD, 36)
    font_text = ImageFont.truetype(FONT_REGULAR, 24)
    font_date = ImageFont.truetype(FONT_REGULAR, 18)

    # ---------- ИМЯ пользователя ----------
    name_text = f"{user.first_name} {user.last_name}"
    y = 250
    text_h = draw_text_centered(name_text, y, font_name)
    y += text_h + 30

    # ---------- Текст "успешно завершил курс" ----------
    completion_text = "успешно завершил(а) курс"
    text_h = draw_text_centered(completion_text, y, font_text)
    y += text_h + 20

    # ---------- Название курса ----------
    course_text = f"«{course.title}»"
    text_h = draw_text_centered(course_text, y, font_course)
    y += text_h + 40

    # ---------- Дата ----------
    issued_date = datetime.utcnow().strftime('%d.%m.%Y')
    date_text = f"Дата выдачи: {issued_date}"
    draw_text_centered(date_text, height - 100, font_date)

    # ---------- Сохраняем изображение ----------
    filename = f"certificate_{user.id_user}_{course.id_course}.png"
    file_path = os.path.join(CERT_DIR, filename)
    img.save(file_path)

    # ---------- Записываем в БД ----------
    certificate = Certificate(
        id_user=user.id_user,
        id_course=course.id_course,
        issued_date=datetime.utcnow(),
        file_path=f"certificates/generated/{filename}"
    )
    db.session.add(certificate)
    db.session.commit()

    return certificate.file_path
