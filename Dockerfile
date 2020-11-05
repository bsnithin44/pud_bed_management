From python:3.7

RUN mkdir /home/pud_bed_management/
WORKDIR /home/pud_bed_management/
COPY static /home/pud_bed_management/static/
COPY templates /home/pud_bed_management/templates/
COPY data.csv patient.csv mysecrets.py requirements.txt /home/pud_bed_management/


RUN pip install -r requirements.txt
COPY main.py run.sh /home/pud_bed_management/
CMD ["/bin/bash", "/home/pud_bed_management/run.sh"]
