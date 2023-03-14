FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY upload-trips.py upload-trips.py
ENTRYPOINT [ "python", "upload-trips.py" ]
