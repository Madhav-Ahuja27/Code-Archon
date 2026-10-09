# Module: `src/flask/globals.py`

**Path:** `C:\temp\flask\src\flask\globals.py`
**Lines:** 62
**Avg Complexity:** 2.0


## Description

flask.globals
~~~~~~~~~~~~~

Defines all the global objects that are proxies to the current
active context.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `functools.partial`

- `werkzeug.local.LocalProxy`

- `werkzeug.local.LocalStack`



## Functions


### `_lookup_req_object(name) → None`



- **Line:** 35–39
- **Complexity:** 2
- **Calls:** getattr, RuntimeError


### `_lookup_app_object(name) → None`



- **Line:** 42–46
- **Complexity:** 2
- **Calls:** getattr, RuntimeError


### `_find_app() → None`



- **Line:** 49–53
- **Complexity:** 2
- **Calls:** RuntimeError



## Classes

