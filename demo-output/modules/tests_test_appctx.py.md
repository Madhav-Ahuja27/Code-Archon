# Module: `tests/test_appctx.py`

**Path:** `C:\temp\flask\tests\test_appctx.py`
**Lines:** 220
**Avg Complexity:** 3.1


## Description

tests.appctx
~~~~~~~~~~~~

Tests the application context.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `pytest`

- `flask`



## Functions


### `test_basic_url_generation(app) → None`



- **Line:** 16–26
- **Complexity:** 2
- **Calls:** route, app_context, url_for


### `index() → None`



- **Line:** 21–22
- **Complexity:** 1
- **Calls:** route


### `test_url_generation_requires_server_name(app) → None`



- **Line:** 29–32
- **Complexity:** 1
- **Calls:** app_context, raises, url_for


### `test_url_generation_without_context_fails() → None`



- **Line:** 35–37
- **Complexity:** 1
- **Calls:** raises, url_for


### `test_request_context_means_app_context(app) → None`



- **Line:** 40–43
- **Complexity:** 3
- **Calls:** test_request_context, _get_current_object


### `test_app_context_provides_current_app(app) → None`



- **Line:** 46–49
- **Complexity:** 3
- **Calls:** app_context, _get_current_object


### `test_app_tearing_down(app) → None`



- **Line:** 52–62
- **Complexity:** 2
- **Calls:** append, app_context


### `cleanup(exception) → None`



- **Line:** 56–57
- **Complexity:** 1
- **Calls:** append


### `test_app_tearing_down_with_previous_exception(app) → None`



- **Line:** 65–80
- **Complexity:** 3
- **Calls:** append, Exception, app_context


### `cleanup(exception) → None`



- **Line:** 69–70
- **Complexity:** 1
- **Calls:** append


### `test_app_tearing_down_with_handled_exception_by_except_block(app) → None`



- **Line:** 83–96
- **Complexity:** 3
- **Calls:** append, app_context, Exception


### `cleanup(exception) → None`



- **Line:** 87–88
- **Complexity:** 1
- **Calls:** append


### `test_app_tearing_down_with_handled_exception_by_app_handler(app, client) → None`



- **Line:** 99–118
- **Complexity:** 2
- **Calls:** route, errorhandler, append, Exception, jsonify, app_context, get, str


### `cleanup(exception) → None`



- **Line:** 104–105
- **Complexity:** 1
- **Calls:** append


### `index() → None`



- **Line:** 108–109
- **Complexity:** 1
- **Calls:** route, Exception


### `handler(f) → None`



- **Line:** 112–113
- **Complexity:** 1
- **Calls:** errorhandler, jsonify, str


### `test_app_tearing_down_with_unhandled_exception(app, client) → None`



- **Line:** 121–139
- **Complexity:** 4
- **Calls:** route, isinstance, append, Exception, raises, len, str, app_context, get


### `cleanup(exception) → None`



- **Line:** 126–127
- **Complexity:** 1
- **Calls:** append


### `index() → None`



- **Line:** 130–131
- **Complexity:** 1
- **Calls:** route, Exception


### `test_app_ctx_globals_methods(app, app_ctx) → None`



- **Line:** 142–162
- **Complexity:** 10
- **Calls:** setdefault, get, pop, raises, list, repr


### `test_custom_app_ctx_globals_class(app) → None`



- **Line:** 165–172
- **Complexity:** 2
- **Calls:** app_context, render_template_string


### `__init__(self) → None`



- **Line:** 167–168
- **Complexity:** 1
- **Calls:** none


### `test_context_refcounts(app, client) → None`



- **Line:** 175–198
- **Complexity:** 4
- **Calls:** route, get, append


### `teardown_req(error) → None`



- **Line:** 179–180
- **Complexity:** 1
- **Calls:** append


### `teardown_app(error) → None`



- **Line:** 183–184
- **Complexity:** 1
- **Calls:** append


### `index() → None`



- **Line:** 187–193
- **Complexity:** 1
- **Calls:** route


### `test_clean_pop(app) → None`



- **Line:** 201–220
- **Complexity:** 4
- **Calls:** append, test_request_context


### `teardown_req(error) → None`



- **Line:** 206–207
- **Complexity:** 1
- **Calls:** none


### `teardown_app(error) → None`



- **Line:** 210–211
- **Complexity:** 1
- **Calls:** append



## Classes


### `CustomRequestGlobals`



- **Bases:** object
- **Methods:** __init__

