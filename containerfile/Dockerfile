# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies required for lxml, Ollama, and other packages
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama for Linux and pull the model ahead of runtime
RUN curl -sSL https://ollama.com/install.sh | sh
RUN ollama pull maxkerkula/megabeam-mistral-7b-512k-q6_k_l:latest

# Copy the entire project into the container
COPY . .

# Set environment variables (can be overridden at runtime)
ENV FILE_PATH="/app/release/akana/inputJson/input.json"
ENV SOURCE_PROCESSED_FILE_PATH="/app/release/akana/output/output.json"
ENV MODEL_NAME="maxkerkula/megabeam-mistral-7b-512k-q6_k_l:latest"

# Expose Ollama default port
EXPOSE 11434

# Run Ollama serve then the Python app
CMD ["bash", "-lc", "ollama serve & sleep 5 && python app.py"]
