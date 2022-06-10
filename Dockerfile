FROM continuumio/miniconda3:latest
RUN mkdir -p /script

COPY . /script
RUN chmod +x ./script*

RUN /opt/conda/bin/conda env create -f /script/requirements.yml

ENV PATH /opt/conda/envs/log_analyzer/bin:$PATH
RUN echo 'source activate log_analyzer' >~/.bashrc

WORKDIR /script
