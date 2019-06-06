FROM python:3.6

MAINTAINER Juan Gonzalo Quiroz Cadavid

COPY balancer /balancer

WORKDIR /balancer

RUN pip install -r requirments.txt

CMD ["python3.6","lb_3_alpha.py"]