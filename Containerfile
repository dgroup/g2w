# @todo #/DEV switch to lightweight python:3.8.5-alpine docker image
FROM python:3.8.5
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["g2w"]
