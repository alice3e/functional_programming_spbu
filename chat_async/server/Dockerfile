# Используем Python образ
FROM python:3.9

# Копируем файлы
WORKDIR /app
COPY server.py .

# Устанавливаем зависимости (если нужно)
RUN pip install --no-cache-dir asyncio

# Запускаем сервер
CMD ["python", "server.py"]
