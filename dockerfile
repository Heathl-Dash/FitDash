FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./fitCore /app/fitCore
COPY ./fitDash /app/fitDash
COPY manage.py /app/
EXPOSE 8000
RUN python manage.py makemigrations
