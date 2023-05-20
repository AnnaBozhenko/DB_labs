FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dump.py .
COPY generate_queries.py .

ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "dump.py"]
