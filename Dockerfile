FROM continuumio/miniconda3:latest
RUN mkdir -p /script
RUN mkdir -p /data

COPY . /script
COPY ./data /data
RUN chmod +x ./script*

RUN /opt/conda/bin/conda env create -f /script/requirements.yml

ENV PATH /opt/conda/envs/log_analyzer/bin:$PATH
RUN echo 'source activate log_analyzer' >~/.bashrc

WORKDIR /script
