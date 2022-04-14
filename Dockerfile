FROM python:3.7
WORKDIR /app
COPY ./app ./
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
CMD kopf run /app/v1.py --verbose