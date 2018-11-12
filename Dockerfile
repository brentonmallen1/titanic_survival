FROM continuumio/miniconda3:latest
MAINTAINER Brenton Mallen (brentonmallen1@gmail.com)

COPY . .
RUN apt-get update && \
    conda env update
ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH
EXPOSE 5000

CMD /opt/conda/envs/titanic/bin/python titanic.py

