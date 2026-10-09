# Module: `src/flask/logging.py`

**Path:** `C:\temp\flask\src\flask\logging.py`
**Lines:** 109
**Avg Complexity:** 4.5


## Description

flask.logging
~~~~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `__future__.absolute_import`

- `logging`

- `sys`

- `warnings`

- `werkzeug.local.LocalProxy`

- `globals.request`



## Functions


### `wsgi_errors_stream() → None`


Find the most appropriate error stream for the application. If a request
is active, log to ``wsgi.errors``, otherwise use ``sys.stderr``.

If you configure your own :class:`logging.StreamHandler`, you may want to
use this for the stream. If you are using file or dict configuration and
can't import this directly, you can refer to it as
``ext://flask.logging.wsgi_errors_stream``.


- **Line:** 21–30
- **Complexity:** 2
- **Calls:** none


### `has_level_handler(logger) → None`


Check if there is a handler in the logging chain that will handle the
given logger's :meth:`effective level <~logging.Logger.getEffectiveLevel>`.


- **Line:** 33–49
- **Complexity:** 5
- **Calls:** getEffectiveLevel, any


### `_has_config(logger) → None`


Decide if a logger has direct configuration applied by checking
its properties against the defaults.

:param logger: The :class:`~logging.Logger` to inspect.


- **Line:** 60–71
- **Complexity:** 4
- **Calls:** none


### `create_logger(app) → None`


Get the the Flask apps's logger and configure it if needed.

The logger name will be the same as
:attr:`app.import_name <flask.Flask.name>`.

When :attr:`~flask.Flask.debug` is enabled, set the logger level to
:data:`logging.DEBUG` if it is not set.

If there is no handler for the logger's effective level, add a
:class:`~logging.StreamHandler` for
:func:`~flask.logging.wsgi_errors_stream` with a basic format.


- **Line:** 74–109
- **Complexity:** 7
- **Calls:** getLogger, setLevel, has_level_handler, addHandler, _has_config, warn, format



## Classes

