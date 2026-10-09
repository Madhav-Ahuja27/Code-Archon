# Module: `examples/tutorial/tests/test_blog.py`

**Path:** `C:\temp\flask\examples\tutorial\tests\test_blog.py`
**Lines:** 83
**Avg Complexity:** 3.2



## Imports



- `pytest`

- `flaskr.db.get_db`



## Functions


### `test_index(client, auth) → None`



- **Line:** 6–16
- **Complexity:** 7
- **Calls:** get, login


### `test_login_required(client, path) → None`



- **Line:** 20–22
- **Complexity:** 2
- **Calls:** parametrize, post


### `test_author_required(app, client, auth) → None`



- **Line:** 25–37
- **Complexity:** 4
- **Calls:** login, app_context, get_db, execute, commit, post, get


### `test_exists_required(client, auth, path) → None`



- **Line:** 41–43
- **Complexity:** 2
- **Calls:** parametrize, login, post


### `test_create(client, auth, app) → None`



- **Line:** 46–54
- **Complexity:** 3
- **Calls:** login, post, app_context, get_db, get, fetchone, execute


### `test_update(client, auth, app) → None`



- **Line:** 57–65
- **Complexity:** 3
- **Calls:** login, post, app_context, get_db, fetchone, get, execute


### `test_create_update_validate(client, auth, path) → None`



- **Line:** 69–72
- **Complexity:** 2
- **Calls:** parametrize, login, post


### `test_delete(client, auth, app) → None`



- **Line:** 75–83
- **Complexity:** 3
- **Calls:** login, post, app_context, get_db, fetchone, execute



## Classes

