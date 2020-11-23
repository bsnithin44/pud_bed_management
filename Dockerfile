From python:3.7

RUN mkdir /home/pud_bed_management/
WORKDIR /home/pud_bed_management/

COPY app /home/pud_bed_management/app
COPY data.csv run.sh /home/pud_bed_management/

RUN pip install -r requirements.txt
COPY run.sh /home/pud_bed_management/
CMD ["/bin/bash", "/home/pud_bed_management/run.sh"]
