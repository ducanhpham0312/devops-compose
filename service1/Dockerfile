# Use Python base image
FROM python:3.12

RUN pip install Flask requests

COPY service1.py /app/service1.py

WORKDIR /app

EXPOSE 8199

CMD ["python", "service1.py"]
