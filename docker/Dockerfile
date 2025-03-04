FROM continuumio/miniconda3

WORKDIR /app

SHELL ["/bin/bash", "--login", "-c"]

COPY api_env.yaml .
RUN conda env create -f api_env.yaml

RUN conda init bash

RUN conda activate nets

COPY app.py .
ENTRYPOINT ["python3", "app.py"]
