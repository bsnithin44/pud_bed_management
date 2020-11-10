From python:3.7

RUN mkdir /home/pud_bed_management/
WORKDIR /home/pud_bed_management/

COPY templates /home/pud_bed_management/templates/
COPY data.csv patient.csv mysecrets.py requirements.txt /home/pud_bed_management/
COPY auth.py crud.py models.py database.py schemas.py main.py /home/pud_bed_management/

RUN pip install -r requirements.txt
COPY run.sh /home/pud_bed_management/
CMD ["/bin/bash", "/home/pud_bed_management/run.sh"]
