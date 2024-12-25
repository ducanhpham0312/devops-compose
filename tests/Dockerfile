FROM python:3.12

WORKDIR /app

RUN pip install requests

EXPOSE 8197

COPY test_app.py /app/tests/test_app.py

CMD ["python3", "-m", "unittest", "discover", "-s", "/app/tests", "-p", "test_*.py"]
