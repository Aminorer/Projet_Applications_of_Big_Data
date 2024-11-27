FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into /app
COPY . /app

# Expose volumes for input and output directories
VOLUME ["/input", "/output"]

# Set environment variables for input and output directories
ENV INPUT_DIR=/input
ENV OUTPUT_DIR=/output

# Define the command to run when the container starts
CMD ["python", "/app/predict.py", "--input_dir", "/input", "--output_dir", "/output"]
