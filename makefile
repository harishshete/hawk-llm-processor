APP_NAME := hawk-llm-processor
VERSION := 0.1.2
REGISTRY := immnan
IMAGE := $(REGISTRY)/hawk-llm

DOCKERFILE := containerfile/Dockerfile
PYTHON := python3

.PHONY: help install compile-pyc build-image push-image release clean

help:
	@echo "Available targets:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make compile-pyc  - Precompile project Python files into .pyc"
	@echo "  make build-image  - Build container image and tag $(IMAGE):$(VERSION), $(IMAGE):latest"
	@echo "  make push-image   - Push both image tags to Docker registry"
	@echo "  make release      - Build image and push both tags"
	@echo "  make clean        - Remove local build artifacts"

install:
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Python dependencies installed"

compile-pyc:
	$(PYTHON) -m compileall -q app.py utils
	@echo "Generated Python bytecode for project files"

build-image: compile-pyc
	docker buildx build \
		--load \
		-f $(DOCKERFILE) \
		-t $(IMAGE):$(VERSION) \
		-t $(IMAGE):latest \
		.

push-image:
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest

release: build-image push-image

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned up Python artifacts"
