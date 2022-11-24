FROM python

COPY requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt
RUN mkdir /data
COPY main.py /data/main.py
ADD app /data/app

WORKDIR /data
EXPOSE 5000

CMD ["python", "main.py"]