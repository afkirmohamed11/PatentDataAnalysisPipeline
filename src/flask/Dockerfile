FROM python:3.9-slim

WORKDIR /app

ARG LANG='en_us.UTF-8'

COPY . /app

RUN pip3 install Flask
RUN pip3 install gunicorn
RUN pip3 install Jinja2
RUN pip3 install Werkzeug
RUN pip3 install markupsafe
RUN pip3 install pymongo


CMD ["python3", "-m","flask", "run", "--host=0.0.0.0"]