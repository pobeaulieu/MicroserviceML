# Use the official Python image with version 3.8.18 as the base image
FROM python:3.8.18

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential libffi-dev

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container at /app
COPY ./webapp ./webapp
COPY ./microminer ./microminer

CMD ["python", "./webapp/app.py"]
