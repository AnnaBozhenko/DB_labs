FROM python:3.10

WORKDIR /webapp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /webapp/app/
COPY .flaskenv .
COPY .env .
COPY config.py .
COPY run_app.py .

CMD ["python", "run_app.py"]