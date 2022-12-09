# Pull Python image
FROM python:3.9

# Set working directory of image - name folder flaskr
WORKDIR /machine-learning-client

# Add files from machine to Docker image
ADD . /machine-learning-client

# Install dependencies and packages
RUN pip install -r requirements.txt

# TODO: run ml client on 127.0.0.1:6000
CMD ["python3", "-m", "flask", "--app=flaskr", "--debug", "run", "--host=0.0.0.0"]