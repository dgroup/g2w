FROM python:3.8.5-alpine
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["g2w"]
