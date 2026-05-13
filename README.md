# LLM Gateway

A lightweight Python processor that reads exported release data, analyzes HTML changes, and generates a JSON summary using an LLM.

## What it does

- Reads input JSON from `SOURCE_RESULT`
- Detects product and release metadata
- Extracts HTML sections and compares old vs. new articles
- Builds an LLM prompt and calls the configured model
- Writes a summary JSON file to `SOURCE_SHARED_VOLUME_PATH`

## Prerequisites

- Python 3.11+ or compatible Python 3
- `pip` installed
- Docker if you want to run with the container image

## Python dependencies

Install dependencies with:

```bash
python3 -m pip install -r requirements.txt
```

## Environment variables

The app uses these environment variables:

- `SOURCE_RESULT` - path to the input JSON file
- `SOURCE_SHARED_VOLUME_PATH` - path where processed output JSON is written
- `MODEL_NAME` - the LLM model name (default is `maxkerkula/megabeam-mistral-7b-512k-q6_k_l`)

Example:

```bash
export SOURCE_RESULT="./release/akana/inputJson/input.json"
export SOURCE_SHARED_VOLUME_PATH="./release/akana/output/output.json"
export MODEL_NAME="maxkerkula/megabeam-mistral-7b-512k-q6_k_l"
```

## Run locally

```bash
python app.py
```

## Docker

The container image is built from `containerfile/Dockerfile`.
It installs Ollama, pre-pulls the model, starts `ollama serve`, then runs `app.py`.

Build the image with:

```bash
docker build -f containerfile/Dockerfile -t llm-gateway .
```

Run the container with mounted volumes and env vars:

```bash
docker run --rm \
  -v "$(pwd)/release:/app/release" \
  -e SOURCE_RESULT="/app/release/akana/inputJson/input.json" \
  -e SOURCE_SHARED_VOLUME_PATH="/app/release/akana/output/output.json" \
  llm-gateway
```

## Notes

- The input JSON format is expected to match the project export data structure.
- Output JSON includes `title`, `source_name`, `commit_id`, `link`, `what_changed`, `product_name`, and `tag`.
- The Docker setup uses `ollama` and a Linux-compatible install flow.
