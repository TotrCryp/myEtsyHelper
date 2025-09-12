FROM python:3.11-slim

# Робоча директорія всередині контейнера
WORKDIR /backend

# Скопіювати requirements і встановити залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопіювати весь бекенд
COPY . .

# Створюємо папку для бази даних
RUN mkdir -p db

# Виставляємо порт
EXPOSE 8000

# Запуск FastAPI через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
