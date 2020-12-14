From python:3.7

RUN mkdir /home/pud_bed_management/
WORKDIR /home/pud_bed_management/

COPY app /home/pud_bed_management/app
COPY data.csv run.sh requirements.txt /home/pud_bed_management/

RUN mkdir /home/pud_bed_management/configs
COPY config.json /home/pud_bed_management/configs/

RUN pip install -r requirements.txt

CMD ["/bin/bash", "/home/pud_bed_management/run.sh"]
