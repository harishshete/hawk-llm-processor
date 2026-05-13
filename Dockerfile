# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies required for lxml and other packages
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set environment variables (can be overridden at runtime)
ENV FILE_PATH="/app/release/akana/inputJson/input.json"
ENV SOURCE_PROCESSED_FILE_PATH="/app/release/akana/output/output.json"
ENV MODEL_NAME="maxkerkula/megabeam-mistral-7b-512k-q6_k_l"

# Run the application
CMD ["python", "app.py"]
