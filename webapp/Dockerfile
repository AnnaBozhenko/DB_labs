FROM python:3.10

WORKDIR /webapp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /webapp/app/
COPY .flaskenv .
RUN pip install python-dotenv

COPY app.config .
COPY config.py .
COPY dump_testing.py .
COPY generate_queries.py .
COPY app.py .

EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]