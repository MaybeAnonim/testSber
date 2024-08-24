FROM python:3.12.0

WORKDIR /app

COPY requirements.txt .
COPY s1/ s1/
COPY config.py .
COPY .env .
COPY app.db .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "s1/main.py"]