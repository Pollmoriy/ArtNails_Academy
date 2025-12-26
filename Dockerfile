# Dockerfile
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    build-essential \
    default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Открываем порт
EXPOSE 5000

# Запуск приложения
CMD ["python", "run.py"]
