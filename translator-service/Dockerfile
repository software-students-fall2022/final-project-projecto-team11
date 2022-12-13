# Pull Python image
FROM python:3.9

# Set working directory of image - name folder flaskr
WORKDIR /translator-service

# Add files from machine to Docker image
ADD . /translator-service

# Install ffmpeg into the image
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg

# Install dependencies and packages
RUN pip install -r requirements.txt

# TODO: run ml client on 127.0.0.1:6000
CMD ["python3", "-m", "flask", "--app=translator", "run", "--host=0.0.0.0"]