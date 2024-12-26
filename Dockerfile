FROM python:3.8-slim

RUN apt-get update && apt-get install -y bibutils

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY app.py /app

CMD ["python3", "app.py"]