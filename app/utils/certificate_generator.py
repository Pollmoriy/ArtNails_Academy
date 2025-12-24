import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from app import db
from app.models import Certificate

FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'fonts')
FONT_BOLD = os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf')
FONT_REGULAR = os.path.join(FONT_DIR, 'DejaVuSans.ttf')

CERT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'certificates', 'generated')
os.makedirs(CERT_DIR, exist_ok=True)

def generate_certificate_image(user, course):
    existing_cert = Certificate.query.filter_by(
        id_user=user.id_user,
        id_course=course.id_course
    ).first()
    if existing_cert:
        return existing_cert.file_path

    width, height = 1123, 794
    background_color = (255, 255, 255)
    border_color = (202, 168, 92)  # золотая рамка
    accent_color = (180, 130, 50)  # дополнительный цвет

    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    border_width = 10
    # рамка
    draw.rectangle(
        [border_width//2, border_width//2, width-border_width//2, height-border_width//2],
        outline=border_color,
        width=border_width
    )

    # декоративные линии сверху и снизу
    margin = 50
    for y in [margin, height - margin]:
        draw.line([(100, y), (width-100, y)], fill=accent_color, width=4)
        # маленькие звездочки/точки вдоль линии
        for x in range(120, width-120, 50):
            draw.ellipse([x-3, y-3, x+3, y+3], fill=accent_color)

    # угловые элементы (маленькие треугольники)
    triangle_size = 30
    draw.polygon([(border_width, border_width),
                  (border_width + triangle_size, border_width),
                  (border_width, border_width + triangle_size)], fill=accent_color)
    draw.polygon([(width-border_width, border_width),
                  (width-border_width-triangle_size, border_width),
                  (width-border_width, border_width+triangle_size)], fill=accent_color)
    draw.polygon([(border_width, height-border_width),
                  (border_width+triangle_size, height-border_width),
                  (border_width, height-border_width-triangle_size)], fill=accent_color)
    draw.polygon([(width-border_width, height-border_width),
                  (width-border_width-triangle_size, height-border_width),
                  (width-border_width, height-border_width-triangle_size)], fill=accent_color)

    # ---------- Шрифты ----------
    font_name = ImageFont.truetype(FONT_BOLD, 48)
    font_course = ImageFont.truetype(FONT_BOLD, 36)
    font_text = ImageFont.truetype(FONT_REGULAR, 24)
    font_date = ImageFont.truetype(FONT_REGULAR, 18)

    def draw_text_centered(text, y, font, fill=(0,0,0)):
        bbox = draw.textbbox((0,0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) / 2
        draw.text((x+2, y+2), text, font=font, fill=(150,150,150))  # тень
        draw.text((x, y), text, font=font, fill=fill)
        return text_height

    y = 250
    y += draw_text_centered(f"{user.first_name} {user.last_name}", y, font_name) + 30
    y += draw_text_centered("успешно завершил(а) курс", y, font_text) + 20
    y += draw_text_centered(f"«{course.title}»", y, font_course) + 40
    issued_date = datetime.utcnow().strftime('%d.%m.%Y')
    draw_text_centered(f"Дата выдачи: {issued_date}", height - 100, font_date)

    # ---------- Сохраняем ----------
    filename = f"certificate_{user.id_user}_{course.id_course}.png"
    file_path = os.path.join(CERT_DIR, filename)
    img.save(file_path)

    certificate = Certificate(
        id_user=user.id_user,
        id_course=course.id_course,
        issued_date=datetime.utcnow(),
        file_path=f"certificates/generated/{filename}"
    )
    db.session.add(certificate)
    db.session.commit()

    return certificate.file_path
