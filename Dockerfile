# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /src
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run sandbox.py when the container launches
CMD ["python", "sandbox.py"]
