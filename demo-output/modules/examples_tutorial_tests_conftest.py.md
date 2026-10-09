# Module: `examples/tutorial/tests/conftest.py`

**Path:** `C:\temp\flask\examples\tutorial\tests\conftest.py`
**Lines:** 62
**Avg Complexity:** 1.1



## Imports



- `os`

- `tempfile`

- `pytest`

- `flaskr.create_app`

- `flaskr.db.get_db`

- `flaskr.db.init_db`



## Functions


### `app() → None`


Create and configure a new app instance for each test.


- **Line:** 16–32
- **Complexity:** 1
- **Calls:** mkstemp, create_app, close, unlink, app_context, init_db, executescript, get_db


### `client(app) → None`


A test client for the app.


- **Line:** 36–38
- **Complexity:** 1
- **Calls:** test_client


### `runner(app) → None`


A test runner for the app's Click commands.


- **Line:** 42–44
- **Complexity:** 1
- **Calls:** test_cli_runner


### `__init__(self, client) → None`



- **Line:** 48–49
- **Complexity:** 1
- **Calls:** none


### `login(self, username, password) → None`



- **Line:** 51–54
- **Complexity:** 1
- **Calls:** post


### `logout(self) → None`



- **Line:** 56–57
- **Complexity:** 1
- **Calls:** get


### `auth(client) → None`



- **Line:** 61–62
- **Complexity:** 1
- **Calls:** AuthActions



## Classes


### `AuthActions`



- **Bases:** object
- **Methods:** __init__, login, logout

