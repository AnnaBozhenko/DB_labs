FROM python:3.10
WORKDIR /result_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY res_lab2.py .


ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "res_lab2.py"]
