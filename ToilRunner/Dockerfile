# TOIL CONTAINER
FROM python:3.7
# FROM ubuntu:latest

# ------------------------------------------------------------------------------
# Install Requirements

RUN apt-get update
# RUN apt-get --assume-yes install python3-pip

RUN pip install toil[cwl]
RUN curl -sSL https://get.docker.com/ | sh
RUN pip install docker
# RUN apt --assume-yes install docker.io

# ------------------------------------------------------------------------------
# CWL and Toil Setup

# WORKDIR /ToilRunner
# COPY ToilRunner/example.cwl /ToilRunner/example.cwl
# COPY ToilRunner/example-job.yaml /ToilRunner/example-job.yaml

# RUN toil-cwl-runner example.cwl example-job.yaml
# RUN cat ./output.txt

# WORKDIR /output/toy
# WORKDIR /output/simple
# WORKDIR /output/simulation

# # Start docker running
# RUN service docker start

# ------------------------------------------------------------------------------
# Reset work directory

# WORKDIR /