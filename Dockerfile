FROM python:3.9

RUN pip install --upgrade pip
RUN pip install pandas

ENTRYPOINT [ "bash" ]