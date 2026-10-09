# Module: `examples/tutorial/flaskr/blog.py`

**Path:** `C:\temp\flask\examples\tutorial\flaskr\blog.py`
**Lines:** 125
**Avg Complexity:** 2.8



## Imports



- `flask.Blueprint`

- `flask.flash`

- `flask.g`

- `flask.redirect`

- `flask.render_template`

- `flask.request`

- `flask.url_for`

- `werkzeug.exceptions.abort`

- `flaskr.auth.login_required`

- `flaskr.db.get_db`



## Functions


### `index() → None`


Show all the posts, most recent first.


- **Line:** 17–25
- **Complexity:** 1
- **Calls:** route, get_db, fetchall, render_template, execute


### `get_post(id, check_author) → None`


Get a post and its author by id.

Checks that the id exists and optionally that the current user is
the author.

:param id: id of post to get
:param check_author: require the current user to be the author
:return: the post with author information
:raise 404: if a post with the given id doesn't exist
:raise 403: if the current user isn't the author


- **Line:** 28–57
- **Complexity:** 4
- **Calls:** fetchone, abort, execute, format, get_db


### `create() → None`


Create a new post for the current user.


- **Line:** 62–83
- **Complexity:** 4
- **Calls:** route, render_template, flash, get_db, execute, commit, redirect, url_for


### `update(id) → None`


Update a post if the current user is the author.


- **Line:** 88–110
- **Complexity:** 4
- **Calls:** route, get_post, render_template, flash, get_db, execute, commit, redirect, url_for


### `delete(id) → None`


Delete a post.

Ensures that the post exists and that the logged in user is the
author of the post.


- **Line:** 115–125
- **Complexity:** 1
- **Calls:** route, get_post, get_db, execute, commit, redirect, url_for



## Classes

