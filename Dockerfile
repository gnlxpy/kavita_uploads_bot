# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY . .

# Устанавливаем переменные окружения
ENV BOT_TOKEN=""

# Запускаем приложение
CMD ["python", "main.py"]
