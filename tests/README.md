# Tests setup

- On test fusionpbx create a domain 'fusionpbx-pilot.pytest'
- Create a superadmin user and set permissions to delete domains to superadmin group
- Add at least one extension to domain 'fusionpbx-pilot.pytest'
- Copy .env.sample to .env and set the following variables:

``` .env
PYTEST_URL = https://mytesturl
PYTEST_USERNAME = myuser@fusionpbx-pilot.pytest
PYTEST_PASSWORD = mypassword
```

## Running the tests

- Install [uv](https://docs.astral.sh/uv/guides/install-python/)
- Run the pytest using uv:

``` bash
uv run pytest -vvv
```

It will create a virtual environment, if doesn't exists, run pytest.
