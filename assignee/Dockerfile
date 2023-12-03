# Используем базовый образ Python 3.10
FROM python:3.10

# Выбор рабочей директории
WORKDIR /app

# Копируем файл зависимостей
COPY ./AssigneeMicroservice/requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Копируем код приложения
COPY ./AssigneeMicroservice /app

# Определяем порт
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
