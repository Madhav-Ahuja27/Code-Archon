# Module: `examples/tutorial/tests/test_auth.py`

**Path:** `C:\temp\flask\examples\tutorial\tests\test_auth.py`
**Lines:** 69
**Avg Complexity:** 3.0



## Imports



- `pytest`

- `flask.g`

- `flask.session`

- `flaskr.db.get_db`



## Functions


### `test_register(client, app) → None`



- **Line:** 8–21
- **Complexity:** 4
- **Calls:** post, app_context, get, fetchone, execute, get_db


### `test_register_validate_input(client, username, password, message) → None`



- **Line:** 32–36
- **Complexity:** 2
- **Calls:** parametrize, post


### `test_login(client, auth) → None`



- **Line:** 39–52
- **Complexity:** 5
- **Calls:** login, get


### `test_login_validate_input(auth, username, password, message) → None`



- **Line:** 59–61
- **Complexity:** 2
- **Calls:** parametrize, login


### `test_logout(client, auth) → None`



- **Line:** 64–69
- **Complexity:** 2
- **Calls:** login, logout



## Classes

