.PHONY: install smoke api ui ui-headless test report docker-build docker-run

install:
	pip install -r requirements.txt

smoke:
	pytest -m smoke

api:
	pytest tests/api

ui:
	pytest tests/ui

ui-headless:
	HEADLESS=true pytest tests/ui

test:
	pytest

report:
	mkdir -p docs
	pytest --html=docs/report.html --self-contained-html

docker-build:
	docker build -t qa-automation .

docker-run:
	docker run --rm qa-automation