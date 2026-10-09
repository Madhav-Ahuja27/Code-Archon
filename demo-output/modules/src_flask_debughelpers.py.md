# Module: `src/flask/debughelpers.py`

**Path:** `C:\temp\flask\src\flask\debughelpers.py`
**Lines:** 183
**Avg Complexity:** 3.8


## Description

flask.debughelpers
~~~~~~~~~~~~~~~~~~

Various helpers to make the development experience better.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `os`

- `warnings.warn`

- `_compat.implements_to_string`

- `_compat.text_type`

- `app.Flask`

- `blueprints.Blueprint`

- `globals._request_ctx_stack`



## Functions


### `__init__(self, request, key) → None`



- **Line:** 33–48
- **Complexity:** 2
- **Calls:** getlist, join, append


### `__str__(self) → None`



- **Line:** 50–51
- **Complexity:** 1
- **Calls:** none


### `__init__(self, request) → None`



- **Line:** 60–83
- **Complexity:** 2
- **Calls:** append, __init__, encode, split, join


### `attach_enctype_error_multidict(request) → None`


Since Flask 0.8 we're monkeypatching the files object in case a
request is detected that does not use multipart form data but the files
object is accessed.


- **Line:** 86–104
- **Complexity:** 1
- **Calls:** __getitem__, DebugFilesKeyError


### `__getitem__(self, key) → None`



- **Line:** 94–100
- **Complexity:** 1
- **Calls:** __getitem__, DebugFilesKeyError


### `_dump_loader_info(loader) → None`



- **Line:** 107–121
- **Complexity:** 8
- **Calls:** sorted, items, startswith, isinstance, all, type


### `explain_template_loading_attempts(app, template, attempts) → None`


This should help developers understand what failed


- **Line:** 124–169
- **Complexity:** 13
- **Calls:** enumerate, info, isinstance, append, _dump_loader_info, join, repr


### `explain_ignored_app_run() → None`



- **Line:** 172–183
- **Complexity:** 2
- **Calls:** get, warn, Warning



## Classes


### `UnexpectedUnicodeError`


Raised in places where we want some better error reporting for
unexpected unicode or binary data.


- **Bases:** AssertionError, UnicodeError
- **Methods:** none


### `DebugFilesKeyError`


Raised from request.files during debugging.  The idea is that it can
provide a better error message than just a generic KeyError/BadRequest.


- **Bases:** KeyError, AssertionError
- **Methods:** __init__, __str__


### `FormDataRoutingRedirect`


This exception is raised by Flask in debug mode if it detects a
redirect caused by the routing system when the request method is not
GET, HEAD or OPTIONS.  Reasoning: form data will be dropped.


- **Bases:** AssertionError
- **Methods:** __init__


### `newcls`



- **Bases:** oldcls
- **Methods:** __getitem__

