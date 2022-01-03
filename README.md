# Seam for Python

Control locks, lights and other internet of things devices with Seam's simple API. Check out the [documentation](https://docs.getseam.com) or [some examples](examples)

## Setup

```bash
pip install seamapi
```

## Usage

```python
from seamapi import Seam

# export SEAM_API_KEY=***
seam = Seam()

some_lock = seam.locks.get(
  name="Front Door",
  location="123 Amy Lane"
)

seam.locks.lock_door(some_lock)
```

## Development

This project uses [poetry](https://github.com/python-poetry/poetry)

- To run tests, run `poetry run pytest`
- To build the project for publishing, run `poetry build`
- To publish the project run `poetry build`

Our tests use a seam sandbox environment given by the environment
variables `SEAM_SANDBOX_API_KEY`. If you want to run the tests, you should
first create a sandbox workspace [on your dashboard](https://dashboard.getseam.com)
then create a sandbox workspace.
