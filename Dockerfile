FROM ubuntu:jammy

RUN apt update && apt install -y python3 python3-pip 

COPY requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt

ADD app /app

WORKDIR /app
EXPOSE 8000

CMD python3 -m uvicorn api:app --host 0.0.0.0 --port 8000