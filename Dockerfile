# Use the official Python image with version 3.8.18 as the base image
FROM python:3.8.18

# Set the working directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential libffi-dev

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container at /app
COPY ./webapp ./webapp

# Command to run on container start
WORKDIR /app/webapp
CMD ["python", "microminer.py"]
