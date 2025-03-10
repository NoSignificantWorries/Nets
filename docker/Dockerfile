FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "nets2", "/bin/bash", "-c"]

EXPOSE 5555

COPY *.py .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "nets2", "python", "app.py"]
