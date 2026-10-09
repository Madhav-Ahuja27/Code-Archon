# Module: `tests/test_reqctx.py`

**Path:** `C:\temp\flask\tests\test_reqctx.py`
**Lines:** 285
**Avg Complexity:** 3.2


## Description

tests.reqctx
~~~~~~~~~~~~

Tests the request context.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `pytest`

- `flask`

- `flask.sessions.SessionInterface`

- `greenlet.greenlet`

- `flask.testing.EnvironBuilder`

- `flask.testing.EnvironBuilder`



## Functions


### `test_teardown_on_pop(app) → None`



- **Line:** 22–33
- **Complexity:** 3
- **Calls:** test_request_context, push, pop, append


### `end_of_request(exception) → None`



- **Line:** 26–27
- **Complexity:** 1
- **Calls:** append


### `test_teardown_with_previous_exception(app) → None`



- **Line:** 36–50
- **Complexity:** 4
- **Calls:** append, Exception, test_request_context


### `end_of_request(exception) → None`



- **Line:** 40–41
- **Complexity:** 1
- **Calls:** append


### `test_teardown_with_handled_exception(app) → None`



- **Line:** 53–66
- **Complexity:** 4
- **Calls:** append, test_request_context, Exception


### `end_of_request(exception) → None`



- **Line:** 57–58
- **Complexity:** 1
- **Calls:** append


### `test_proper_test_request_context(app) → None`



- **Line:** 69–107
- **Complexity:** 3
- **Calls:** update, route, test_request_context, warns, url_for


### `index() → None`



- **Line:** 73–74
- **Complexity:** 1
- **Calls:** route


### `sub() → None`



- **Line:** 77–78
- **Complexity:** 1
- **Calls:** route


### `test_context_binding(app) → None`



- **Line:** 110–123
- **Complexity:** 4
- **Calls:** route, test_request_context, index, meh


### `index() → None`



- **Line:** 112–113
- **Complexity:** 1
- **Calls:** route


### `meh() → None`



- **Line:** 116–117
- **Complexity:** 1
- **Calls:** route


### `test_context_test(app) → None`



- **Line:** 126–135
- **Complexity:** 5
- **Calls:** test_request_context, push, has_request_context, pop


### `test_manual_context_binding(app) → None`



- **Line:** 138–148
- **Complexity:** 2
- **Calls:** route, test_request_context, push, pop, index, raises


### `index() → None`



- **Line:** 140–141
- **Complexity:** 1
- **Calls:** route


### `test_greenlet_context_copying(self, app, client) → None`



- **Line:** 153–180
- **Complexity:** 3
- **Calls:** route, get, run, copy, append, greenlet


### `index() → None`



- **Line:** 157–174
- **Complexity:** 1
- **Calls:** route, copy, append, greenlet, get


### `g() → None`



- **Line:** 161–171
- **Complexity:** 1
- **Calls:** get


### `test_greenlet_context_copying_api(self, app, client) → None`



- **Line:** 182–205
- **Complexity:** 3
- **Calls:** route, get, run, append, greenlet


### `index() → None`



- **Line:** 186–199
- **Complexity:** 1
- **Calls:** route, append, greenlet, get


### `g() → None`



- **Line:** 190–196
- **Complexity:** 1
- **Calls:** get


### `test_session_error_pops_context() → None`



- **Line:** 208–229
- **Complexity:** 4
- **Calls:** CustomFlask, route, get, FailingSessionInterface, AssertionError, SessionError, test_client


### `open_session(self, app, request) → None`



- **Line:** 213–214
- **Complexity:** 1
- **Calls:** SessionError


### `index() → None`



- **Line:** 222–224
- **Complexity:** 1
- **Calls:** route, AssertionError


### `test_bad_environ_raises_bad_request() → None`



- **Line:** 232–249
- **Complexity:** 2
- **Calls:** Flask, EnvironBuilder, get_environ, request_context, full_dispatch_request


### `test_environ_for_valid_idna_completes() → None`



- **Line:** 252–274
- **Complexity:** 2
- **Calls:** Flask, route, EnvironBuilder, get_environ, request_context, full_dispatch_request


### `index() → None`



- **Line:** 256–257
- **Complexity:** 1
- **Calls:** route


### `test_normal_environ_completes() → None`



- **Line:** 277–285
- **Complexity:** 2
- **Calls:** Flask, route, get, test_client


### `index() → None`



- **Line:** 281–282
- **Complexity:** 1
- **Calls:** route



## Classes


### `TestGreenletContextCopying`



- **Bases:** object
- **Methods:** test_greenlet_context_copying, test_greenlet_context_copying_api


### `SessionError`



- **Bases:** Exception
- **Methods:** none


### `FailingSessionInterface`



- **Bases:** SessionInterface
- **Methods:** open_session


### `CustomFlask`



- **Bases:** flask.Flask
- **Methods:** none

