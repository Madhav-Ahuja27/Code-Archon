# Module: `tests/test_converters.py`

**Path:** `C:\temp\flask\tests\test_converters.py`
**Lines:** 40
**Avg Complexity:** 2.5



## Imports



- `werkzeug.routing.BaseConverter`

- `flask.has_request_context`

- `flask.url_for`



## Functions


### `test_custom_converters(app, client) → None`



- **Line:** 7–25
- **Complexity:** 3
- **Calls:** route, join, test_request_context, split, get, url_for, super, base_to_url


### `to_python(self, value) → None`



- **Line:** 9–10
- **Complexity:** 1
- **Calls:** split


### `to_url(self, value) → None`



- **Line:** 12–14
- **Complexity:** 1
- **Calls:** join, super, base_to_url


### `index(args) → None`



- **Line:** 19–20
- **Complexity:** 1
- **Calls:** route, join


### `test_context_available(app, client) → None`



- **Line:** 28–40
- **Complexity:** 2
- **Calls:** route, has_request_context, get


### `to_python(self, value) → None`



- **Line:** 30–32
- **Complexity:** 1
- **Calls:** has_request_context


### `index(name) → None`



- **Line:** 37–38
- **Complexity:** 1
- **Calls:** route



## Classes


### `ListConverter`



- **Bases:** BaseConverter
- **Methods:** to_python, to_url


### `ContextConverter`



- **Bases:** BaseConverter
- **Methods:** to_python

