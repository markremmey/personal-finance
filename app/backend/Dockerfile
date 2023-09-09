# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the maintainer label
LABEL maintainer="mremmey7@gmail.com"

# Set environment variables
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set the working directory in docker
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./display_records.py /app/
COPY ./requirements.txt /app/
COPY ./data /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

# Specify the default command to run on boot
CMD ["gunicorn", "display_records:app", "--bind", "0.0.0.0:5000"]