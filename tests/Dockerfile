FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir requests unittest-xml-reporting

EXPOSE 8197

COPY test_app.py /app/tests/test_app.py

CMD ["python3", "-m", "unittest", "discover", "-s", "/app/tests", "-p", "test_*.py"]
