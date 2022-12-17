# Pull Python image
FROM --platform=linux/amd64 python:3.9

# Set working directory of image - name folder flaskr
WORKDIR /web-app

# Add files from machine to Docker image
ADD . /web-app

# Install dependencies and packages
RUN pip install -r requirements.txt

# run flask app on 127.0.0.1:5001
CMD ["python3", "-m", "flask", "--app=app", "run", "--host=0.0.0.0", "--port", "5001"]