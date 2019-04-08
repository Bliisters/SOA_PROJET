FROM python:3.7.0
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y mongodb-org
CMD ["python","Users.py"]
