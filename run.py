from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Проверяем подключение
    print("🔗 Подключение к базе данных:", db.engine.url)

    # Используем text() для SQL-запроса
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE();"))
        current_db = result.fetchone()[0]
        print("🏷 Используемая база данных:", current_db)

    # Список таблиц до создания
    inspector = db.inspect(db.engine)
    print("📋 Таблицы до create_all():", inspector.get_table_names())

    # Создаём все таблицы
    db.create_all()
    print("✅ db.create_all() вызван")

    # Список таблиц после создания
    print("📋 Таблицы после create_all():", inspector.get_table_names())

# 🔹 Запуск сервера Flask
if __name__ == "__main__":
    app.run(debug=True)
