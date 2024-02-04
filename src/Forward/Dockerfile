FROM python:3.12.1-slim-bookworm
COPY . /app
RUN pip3 install flask requests
ENTRYPOINT ["python", "/app/app.py"]