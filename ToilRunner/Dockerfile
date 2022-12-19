# TOIL CONTAINER
FROM python:3.7

# ------------------------------------------------------------------------------
# Install Requirements


RUN pip install toil[cwl]
RUN curl -sSL https://get.docker.com/ | sh

# ------------------------------------------------------------------------------
# CWL and Toil Setup

WORKDIR /toil

# ------------------------------------------------------------------------------
# Reset work directory

WORKDIR /