#specify image
FROM python:latest

#expose port
EXPOSE 8050

#set working direct0ry as app
WORKDIR /app

#Need to ensure gcc is in docker container?
#RUN yum update -y
#RUN yum groupinstall 'Development Tools' -y
#copy requirements file
COPY requirements.txt requirements.txt
#install
RUN pip3 install -r requirements.txt
#copy everything else
COPY . .
#run command
CMD ["python","app.py"]
#CMD ["gunicorn","--workers=5","--threads=1","-b 0.0.0.0:80", "server"]