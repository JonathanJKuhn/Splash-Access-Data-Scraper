FROM python:3.11-slim

WORKDIR /app

COPY scraper/ /app/
COPY scraper/requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
