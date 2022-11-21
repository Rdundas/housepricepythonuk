#specify image
FROM python:latest

LABEL maintainer "Richard Dundas"

#expose port
EXPOSE 80

#set working directory as app
RUN mkdir -p /home/python/
WORKDIR '/home/python/'

#Need to ensure gcc is in docker container?
#RUN yum update -y
#RUN yum groupinstall 'Development Tools' -y
#copy requirements file
COPY requirements.txt ./
#Step to update pip
RUN pip3 install --upgrade pip setuptools --user --no-cache-dir
#install
RUN pip3 install -r requirements.txt
#copy everything else, technically don't need with docker-compose-dev but suggest leave in
COPY ./ ./
#run command
#CMD ["python","app/app.py"]
CMD gunicorn --bind 0.0.0.0:8050 app.app:server