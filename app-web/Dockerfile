FROM python:3.12.4

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY serve.py serve.py
CMD ["python", "serve.py"]