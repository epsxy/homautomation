# Python

This package contains all the microservices used to communicate sensors data through all the local network. We use FastAPI and Uvicorn to quickly deploy nodes on each Raspberry Pi.

## Requirements

- Python >= 3.6
- Pipenv

## Install

```bash
pipenv install
```

## Run

```bash
# --host and --port to make the app available on the local network
# add --daemon to run in background
pipenv run uvicorn main:app --host 0.0.0.0 --port 8080
```
# Python scripts

## Environnement file

The environment file is used to provide some configuration values, regarding:

- email address credentials
- database host and port
- enable/disable email notifications
- enable/disable logger

### Usage

Rename `sandbox.env` to `.env` and complete it with your own credentials and parameters.
```
mv sandbox.env .env
```