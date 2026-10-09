# Module: `tests/test_subclassing.py`

**Path:** `C:\temp\flask\tests\test_subclassing.py`
**Lines:** 31
**Avg Complexity:** 4.0


## Description

tests.subclassing
~~~~~~~~~~~~~~~~~

Test that certain behavior of flask can be customized by
subclasses.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `flask`

- `flask._compat.StringIO`



## Functions


### `test_suppressed_exception_logging() → None`



- **Line:** 16–31
- **Complexity:** 4
- **Calls:** StringIO, SuppressedFlask, route, get, Exception, getvalue, test_client


### `log_exception(self, exc_info) → None`



- **Line:** 18–19
- **Complexity:** 1
- **Calls:** none


### `index() → None`



- **Line:** 25–26
- **Complexity:** 1
- **Calls:** route, Exception



## Classes


### `SuppressedFlask`



- **Bases:** flask.Flask
- **Methods:** log_exception

