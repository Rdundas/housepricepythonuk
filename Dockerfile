#specify image
FROM python:latest

#expose port
EXPOSE 8050

#set working directory as app
WORKDIR /app

#Need to ensure gcc is in docker container?
#RUN yum update -y
#RUN yum groupinstall 'Development Tools' -y
#copy requirements file
COPY app/requirements.txt .
#Step to update pip
RUN pip3 install --upgrade pip setuptools --user --no-cache-dir
#install
RUN pip3 install -r requirements.txt
#copy everything else
COPY . .
#run command
#CMD ["python","app.py"]
CMD ["gunicorn","--workers=5","--threads=1","-b 0.0.0.0:8050", "app.app:server"]