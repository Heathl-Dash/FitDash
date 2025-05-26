FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /app/project
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
EXPOSE 8000
RUN python manage.py makemigrations
