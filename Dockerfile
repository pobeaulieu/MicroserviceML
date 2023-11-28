# Use the official Python image with version 3.8.18 as the base image
FROM python:3.8.18

# Copy the requirements.txt file into the container at /app
COPY requirements_pipeline.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements_pipeline.txt

# Copy the entire project into the container at /app
COPY ./webapp ./webapp
COPY ./microminer ./microminer

CMD ["python", "./webapp/app.py"]
