VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

export GOOGLE_APPLICATION_CREDENTIALS=credentials.json

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

install: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt

upload-rag-corpus:
	python3 deploy/rag-deploy.py

run-agent:
	python3 agent/agent.py