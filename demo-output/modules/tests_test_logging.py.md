# Module: `tests/test_logging.py`

**Path:** `C:\temp\flask\tests\test_logging.py`
**Lines:** 115
**Avg Complexity:** 3.5


## Description

tests.test_logging
~~~~~~~~~~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `logging`

- `sys`

- `pytest`

- `flask._compat.StringIO`

- `flask.logging.default_handler`

- `flask.logging.has_level_handler`

- `flask.logging.wsgi_errors_stream`



## Functions


### `reset_logging(pytestconfig) → None`



- **Line:** 21–41
- **Complexity:** 2
- **Calls:** fixture, getLogger, setLevel, unregister, register


### `test_logger(app) → None`



- **Line:** 44–47
- **Complexity:** 4
- **Calls:** none


### `test_logger_debug(app) → None`



- **Line:** 50–53
- **Complexity:** 3
- **Calls:** none


### `test_existing_handler(app) → None`



- **Line:** 56–59
- **Complexity:** 3
- **Calls:** addHandler, StreamHandler


### `test_wsgi_errors_stream(app, client) → None`



- **Line:** 62–75
- **Complexity:** 4
- **Calls:** route, StringIO, get, error, getvalue, _get_current_object, test_request_context


### `index() → None`



- **Line:** 64–66
- **Complexity:** 1
- **Calls:** route, error


### `test_has_level_handler() → None`



- **Line:** 78–91
- **Complexity:** 5
- **Calls:** getLogger, StreamHandler, addHandler, has_level_handler, setLevel


### `test_log_view_exception(app, client) → None`



- **Line:** 94–106
- **Complexity:** 5
- **Calls:** route, StringIO, get, getvalue, Exception


### `index() → None`



- **Line:** 96–97
- **Complexity:** 1
- **Calls:** route, Exception


### `test_warn_old_config(app, request) → None`



- **Line:** 109–115
- **Complexity:** 2
- **Calls:** getLogger, setLevel, addfinalizer, warns, getEffectiveLevel



## Classes

