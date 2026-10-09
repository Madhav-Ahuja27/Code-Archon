# Module: `examples/tutorial/flaskr/db.py`

**Path:** `C:\temp\flask\examples\tutorial\flaskr\db.py`
**Lines:** 54
**Avg Complexity:** 1.4



## Imports



- `sqlite3`

- `click`

- `flask.current_app`

- `flask.g`

- `flask.cli.with_appcontext`



## Functions


### `get_db() → None`


Connect to the application's configured database. The connection
is unique for each request and will be reused if this is called
again.


- **Line:** 9–20
- **Complexity:** 2
- **Calls:** connect


### `close_db(e) → None`


If this request connected to the database, close the
connection.


- **Line:** 23–30
- **Complexity:** 2
- **Calls:** pop, close


### `init_db() → None`


Clear existing data and create new tables.


- **Line:** 33–38
- **Complexity:** 1
- **Calls:** get_db, open_resource, executescript, decode, read


### `init_db_command() → None`


Clear existing data and create new tables.


- **Line:** 43–46
- **Complexity:** 1
- **Calls:** command, init_db, echo


### `init_app(app) → None`


Register database functions with the Flask app. This is called by
the application factory.


- **Line:** 49–54
- **Complexity:** 1
- **Calls:** teardown_appcontext, add_command



## Classes

