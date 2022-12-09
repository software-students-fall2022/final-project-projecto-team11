# Pull Python image
FROM python:3.9

# Set working directory of image - name folder flaskr
WORKDIR /web-app

# Add files from machine to Docker image
ADD . /web-app

# Install dependencies and packages
RUN pip install -r requirements.txt

# run flask app on 127.0.0.1:5000
CMD ["python3", "-m", "flask", "--app=flaskr", "run", "--host=0.0.0.0"]