# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Ensure Ollama stores keys/models in a writable location at runtime
ENV HOME=/tmp
ENV OLLAMA_HOME=/tmp/.ollama
RUN mkdir -p /tmp/.ollama && chmod 777 /tmp/.ollama

# Install system dependencies required for lxml, Ollama, and other packages
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    zstd \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama for Linux
RUN curl -sSL https://ollama.com/install.sh | sh

# Copy the entire project into the container
COPY . .

# Set environment variables (can be overridden at runtime)
ENV SOURCE_RESULT="/app/release/akana/inputJson/input.json"
ENV SOURCE_PROCESSED_FILE_PATH="/app/release/akana/output/output.json"
ENV MODEL_NAME="maxkerkula/megabeam-mistral-7b-512k-q6_k_l:latest"
ENV API_SERVER="hawk-apiserver-svc:3000"

# Expose Ollama default port
EXPOSE 11434

# Run Ollama, ensure configured model is present, then start the Python app
CMD ["bash", "-lc", "set -e; ollama serve & until ollama list >/dev/null 2>&1; do sleep 1; done; ollama pull \"$MODEL_NAME\"; python app.py"]
