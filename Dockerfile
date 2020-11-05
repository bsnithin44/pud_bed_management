From python:3.7-alpine

RUN mkdir /home/pud_bed_management/
WORKDIR /home/pud_bed_management/
COPY static templates /home/pud_bed_management/
COPY data.csv patient.csv main.py requirements.txt /home/pud_bed_management/


RUN pip install -r requirements.txt

CMD ['bin/bash', "echo hello uvicorn"]