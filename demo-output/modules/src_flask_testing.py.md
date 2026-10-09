# Module: `src/flask/testing.py`

**Path:** `C:\temp\flask\src\flask\testing.py`
**Lines:** 283
**Avg Complexity:** 3.2


## Description

flask.testing
~~~~~~~~~~~~~

Implements test support helpers.  This module is lazily imported
and usually not used in production environments.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `warnings`

- `contextlib.contextmanager`

- `werkzeug.test`

- `click.testing.CliRunner`

- `werkzeug.test.Client`

- `werkzeug.urls.url_parse`

- `_request_ctx_stack`

- `cli.ScriptInfo`

- `json.dumps`



## Functions


### `__init__(self, app, path, base_url, subdomain, url_scheme) → None`



- **Line:** 47–86
- **Complexity:** 1
- **Calls:** __init__, url_parse, format, bool, get, super, lstrip, isinstance


### `json_dumps(self, obj) → None`


Serialize ``obj`` to a JSON-formatted string.

The serialization will be configured according to the config associated
with this EnvironBuilder's ``app``.


- **Line:** 88–95
- **Complexity:** 1
- **Calls:** setdefault, json_dumps


### `make_test_environ_builder() → None`


Create a :class:`flask.testing.EnvironBuilder`.

.. deprecated: 1.1
    Will be removed in 2.0. Construct
    ``flask.testing.EnvironBuilder`` directly instead.


- **Line:** 98–112
- **Complexity:** 1
- **Calls:** warn, EnvironBuilder, DeprecationWarning


### `__init__(self) → None`



- **Line:** 132–137
- **Complexity:** 1
- **Calls:** __init__, super


### `session_transaction(self) → None`


When used in combination with a ``with`` statement this opens a
session transaction.  This can be used to modify the session that
the test client uses.  Once the ``with`` block is left the session is
stored back.

::

    with client.session_transaction() as session:
        session['value'] = 42

Internally this is implemented by going through a temporary test
request context and since session handling could depend on
request variables this function accepts the same arguments as
:meth:`~flask.Flask.test_request_context` which are directly
passed through.


- **Line:** 140–190
- **Complexity:** 4
- **Calls:** setdefault, inject_wsgi, RuntimeError, test_request_context, open_session, push, response_class, get_wsgi_headers, extract_wsgi, pop, is_null_session, save_session


### `open(self) → None`



- **Line:** 192–228
- **Complexity:** 5
- **Calls:** pop, open, isinstance, copy, setdefault, EnvironBuilder, len, update, get_environ, close


### `__enter__(self) → None`



- **Line:** 230–234
- **Complexity:** 2
- **Calls:** RuntimeError


### `__exit__(self, exc_type, exc_value, tb) → None`



- **Line:** 236–249
- **Complexity:** 4
- **Calls:** pop


### `__init__(self, app) → None`



- **Line:** 258–260
- **Complexity:** 1
- **Calls:** __init__, super


### `invoke(self, cli, args) → None`


Invokes a CLI command in an isolated environment. See
:meth:`CliRunner.invoke <click.testing.CliRunner.invoke>` for
full method documentation. See :ref:`testing-cli` for examples.

If the ``obj`` argument is not given, passes an instance of
:class:`~flask.cli.ScriptInfo` that knows how to load the Flask
app being tested.

:param cli: Command object to invoke. Default is the app's
    :attr:`~flask.app.Flask.cli` group.
:param args: List of strings to invoke the command with.

:return: a :class:`~click.testing.Result` object.


- **Line:** 262–283
- **Complexity:** 3
- **Calls:** invoke, ScriptInfo, super



## Classes


### `EnvironBuilder`


An :class:`~werkzeug.test.EnvironBuilder`, that takes defaults from the
application.

:param app: The Flask application to configure the environment from.
:param path: URL path being requested.
:param base_url: Base URL where the app is being served, which
    ``path`` is relative to. If not given, built from
    :data:`PREFERRED_URL_SCHEME`, ``subdomain``,
    :data:`SERVER_NAME`, and :data:`APPLICATION_ROOT`.
:param subdomain: Subdomain name to append to :data:`SERVER_NAME`.
:param url_scheme: Scheme to use instead of
    :data:`PREFERRED_URL_SCHEME`.
:param json: If given, this is serialized as JSON and passed as
    ``data``. Also defaults ``content_type`` to
    ``application/json``.
:param args: other positional arguments passed to
    :class:`~werkzeug.test.EnvironBuilder`.
:param kwargs: other keyword arguments passed to
    :class:`~werkzeug.test.EnvironBuilder`.


- **Bases:** werkzeug.test.EnvironBuilder
- **Methods:** __init__, json_dumps


### `FlaskClient`


Works like a regular Werkzeug test client but has some knowledge about
how Flask works to defer the cleanup of the request context stack to the
end of a ``with`` body when used in a ``with`` statement.  For general
information about how to use this class refer to
:class:`werkzeug.test.Client`.

.. versionchanged:: 0.12
   `app.test_client()` includes preset default environment, which can be
   set after instantiation of the `app.test_client()` object in
   `client.environ_base`.

Basic usage is outlined in the :ref:`testing` chapter.


- **Bases:** Client
- **Methods:** __init__, session_transaction, open, __enter__, __exit__


### `FlaskCliRunner`


A :class:`~click.testing.CliRunner` for testing a Flask app's
CLI commands. Typically created using
:meth:`~flask.Flask.test_cli_runner`. See :ref:`testing-cli`.


- **Bases:** CliRunner
- **Methods:** __init__, invoke

