# -*- mode: makefile -*-

# tools configuration
SHELL := /bin/sh
DOCKER ?= docker

# docker image configuration
IMAGE_NAME ?= slackbox
IMAGE_TAG ?= dev

# registry configuration
REGISTRY_USERNAME ?= admin
REGISTRY_PASSWORD ?= admin
REGISTRY_HOSTNAME ?= localhost

# component tests configuration
TESTED_HOST ?= localhost
TESTED_PORT ?= 8000

.PHONY: init
init: ## initialise local environment
	@scripts/init

.PHONY: serve
serve: ## run local development server
	@scripts/serve --host ${TESTED_HOST} --port ${TESTED_PORT}

.PHONY: lint
lint: ## lint codebase
	@scripts/lint-codebase

.PHONY: tests-unit
tests-unit: ## run unit tests and code coverage
	@poetry run pytest --cov=src/ tests/unit/

.PHONY: tests-integration
tests-integration: ## run integration tests and code coverage
	@poetry run pytest --cov=src tests/integration/

.PHONY: tests-component
tests-component: ## run component tests
	@poetry run pytest tests/component/ --host ${TESTED_HOST} --port ${TESTED_PORT}

.PHONY: tests-contract
tests-contract: ## run contract tests
	@poetry run schemathesis run "openapi.yaml" --checks all --base-url "http://${TESTED_HOST}:${TESTED_PORT}"

.PHONY: build
build: ## build docker image
	@${DOCKER} build -t ${IMAGE_NAME}:${IMAGE_TAG} .

.PHONY: login
login: ## login to docker registry
	@${DOCKER} login --username ${REGISTRY_USERNAME} --password ${REGISTRY_PASSWORD} ${REGISTRY_HOSTNAME}

.PHONY: push
push: ## push docker image on registry
	@${DOCKER} tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY_HOSTNAME}/${IMAGE_NAME}:${IMAGE_TAG}
	@${DOCKER} push ${REGISTRY_HOSTNAME}/${IMAGE_NAME}:${IMAGE_TAG}

.PHONY: run
run:  ## run local server
	@${DOCKER} run --rm --detach \
		--name slackbox \
		--network host \
		${REGISTRY_HOSTNAME}/${IMAGE_NAME}:${IMAGE_TAG}

.PHONY: help
help: ## show this help
	@echo "Usage: make [TARGET ...]"
	@echo "Targets:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'
