FROM python:3-alpine

RUN pip install boto3

COPY entrypoint.py .

ENTRYPOINT [ "/entrypoint.py" ]
