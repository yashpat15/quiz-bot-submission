FROM python:3.11

ENV DockerHOME=/app/
ENV PYTHONDONTWRITEBYTECODE 1  
ENV PYTHONUNBUFFERED 1         

RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME

RUN pip install --upgrade pip

COPY . $DockerHOME

COPY run_server.sh /app/run_server.sh
RUN chmod +x /app/run_server.sh

RUN pip install -r requirements.txt

ENTRYPOINT ["/app/run_server.sh"]
