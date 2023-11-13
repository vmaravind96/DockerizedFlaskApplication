FROM python:3.8-slim-buster

WORKDIR /test_app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN pip3 install -e .

CMD [ "python3", "-m" , "flask", "--app", "flask_app", "run", "--host=0.0.0.0"]