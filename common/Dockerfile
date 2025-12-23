# Use uma imagem base do Python
#FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
#WORKDIR /workspaces/pizza_delivery

# Instala as dependências do worker
# COPY ./requirements/worker.txt .

# COPY ./common/worker-requirements.txt .
# RUN pip install --no-cache-dir -r worker-requirements.txt

# O comando para iniciar o worker será fornecido pelo docker-compose

#----------------------------------------------------------------------

FROM python:3.11-slim

RUN useradd -m workeruser

COPY ./common/worker-requirements.txt .
RUN pip install --no-cache-dir -r worker-requirements.txt
COPY ./common/celery_app.py ./common/
COPY ./common/tasks.py ./common/

RUN chown -R workeruser ./common
USER workeruser

# CMD ["celery", "-A", "common.celery_app","worker", "--loglevel=INFO"]