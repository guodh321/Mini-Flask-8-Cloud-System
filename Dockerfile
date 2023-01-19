FROM python:3.8

WORKDIR /home/tides

ADD requirements.txt .

COPY app.py .
COPY process.py .

COPY stations.csv .
COPY tideReadings.csv .

RUN pip install -r requirements.txt

ENTRYPOINT [ "flask","run","--port","80","--host","0.0.0.0" ]









