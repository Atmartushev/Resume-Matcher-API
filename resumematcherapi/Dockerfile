# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy project files (including requirements.txt)
COPY . /code/

# Install dependencies
RUN pip install -r requirements.txt
