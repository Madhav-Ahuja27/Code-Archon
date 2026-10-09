# Module: `tests/test_regression.py`

**Path:** `C:\temp\flask\tests\test_regression.py`
**Lines:** 97
**Avg Complexity:** 2.3


## Description

tests.regression
~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests regressions.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `gc`

- `sys`

- `threading`

- `pytest`

- `werkzeug.exceptions.NotFound`

- `flask`

- `flask.helpers.safe_join`



## Functions


### `__enter__(self) → None`



- **Line:** 24–36
- **Complexity:** 1
- **Calls:** disable, acquire, collect, len, get_objects


### `__exit__(self, exc_type, exc_value, tb) → None`



- **Line:** 38–44
- **Complexity:** 2
- **Calls:** collect, len, release, enable, get_objects, fail


### `test_memory_consumption() → None`



- **Line:** 47–67
- **Complexity:** 4
- **Calls:** Flask, route, fire, render_template, test_client, get, hasattr, assert_no_leak, range


### `index() → None`



- **Line:** 51–52
- **Complexity:** 1
- **Calls:** route, render_template


### `fire() → None`



- **Line:** 54–58
- **Complexity:** 1
- **Calls:** test_client, get


### `test_safe_join_toplevel_pardir() → None`



- **Line:** 70–74
- **Complexity:** 1
- **Calls:** raises, safe_join


### `test_aborting(app) → None`



- **Line:** 77–97
- **Complexity:** 3
- **Calls:** errorhandler, route, str, abort, Foo, test_client, get, redirect, url_for


### `handle_foo(e) → None`



- **Line:** 82–83
- **Complexity:** 1
- **Calls:** errorhandler, str


### `index() → None`



- **Line:** 86–87
- **Complexity:** 1
- **Calls:** route, abort, redirect, url_for


### `test() → None`



- **Line:** 90–91
- **Complexity:** 1
- **Calls:** route, Foo



## Classes


### `assert_no_leak`



- **Bases:** object
- **Methods:** __enter__, __exit__


### `Foo`



- **Bases:** Exception
- **Methods:** none

