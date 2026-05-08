.PHONY: docker-build docker-run build clean

VERSION := $(shell git rev-parse --short HEAD 2>/dev/null || echo "latest")
CURDIR := $(CURDIR)

NAME = builder
IMAGE := $(NAME):$(VERSION)
IMAGE_NAME := ghcr.io/cobdh/$(IMAGE)

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-upload:
	docker push $(IMAGE_NAME)
