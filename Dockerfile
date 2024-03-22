# Use an official Python runtime as the base image
FROM python:3.10-slim-buster

# Create a dedicated directory for the bot and set the working directory
RUN mkdir -p /app && chown -R $USER:$USER /app
WORKDIR /app

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update the package lists and install required dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    pv \

