FROM python:3.12

WORKDIR /app

COPY stop_service.py /app

RUN pip install flask
RUN pip install docker
EXPOSE 9000

CMD ["python", "stop_service.py"]
