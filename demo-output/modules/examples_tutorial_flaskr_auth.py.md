# Module: `examples/tutorial/flaskr/auth.py`

**Path:** `C:\temp\flask\examples\tutorial\flaskr\auth.py`
**Lines:** 116
**Avg Complexity:** 3.0



## Imports



- `functools`

- `flask.Blueprint`

- `flask.flash`

- `flask.g`

- `flask.redirect`

- `flask.render_template`

- `flask.request`

- `flask.session`

- `flask.url_for`

- `werkzeug.security.check_password_hash`

- `werkzeug.security.generate_password_hash`

- `flaskr.db.get_db`



## Functions


### `login_required(view) → None`


View decorator that redirects anonymous users to the login page.


- **Line:** 19–29
- **Complexity:** 1
- **Calls:** wraps, view, redirect, url_for


### `wrapped_view() → None`



- **Line:** 23–27
- **Complexity:** 1
- **Calls:** wraps, view, redirect, url_for


### `load_logged_in_user() → None`


If a user id is stored in the session, load the user object from
the database into ``g.user``.


- **Line:** 33–43
- **Complexity:** 2
- **Calls:** get, fetchone, execute, get_db


### `register() → None`


Register a new user.

Validates that the username is not already taken. Hashes the
password for security.


- **Line:** 47–81
- **Complexity:** 6
- **Calls:** route, render_template, get_db, flash, execute, commit, redirect, url_for, fetchone, format, generate_password_hash


### `login() → None`


Log in a registered user by adding the user id to the session.


- **Line:** 85–109
- **Complexity:** 5
- **Calls:** route, render_template, get_db, fetchone, flash, clear, redirect, execute, check_password_hash, url_for


### `logout() → None`


Clear the current session, including the stored user id.


- **Line:** 113–116
- **Complexity:** 1
- **Calls:** route, clear, redirect, url_for



## Classes

