## Setup

 - Install [Poetry](https://python-poetry.org/docs/#installation)
 - Install [Redis](https://redis.io/download)
 - Start Redis
```bash
redis-server
```
 - Install dependencies
```bash
poetry install
```

## Running

Run API Server:
```bash
poetry run start
```

Run Celery Task runner:
```bash
poetry run celery -A agent_runner worker --loglevel=INFO
```

Run Celery Beat (Triggers tasks on the task runner based on beat config):
```bash
poetry run celery -A agent_runner beat
```
