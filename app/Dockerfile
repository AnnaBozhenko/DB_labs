FROM python:3.10
# FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# RUN \
#  apk add --no-cache postgresql-libs && \
#  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
#  python3 -m pip install -r requirements.txt --no-cache-dir && \
#  apk --purge del .build-deps

COPY dump.py .
COPY generate_queries.py .

ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "dump.py"]
