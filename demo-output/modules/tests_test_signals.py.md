# Module: `tests/test_signals.py`

**Path:** `C:\temp\flask\tests\test_signals.py`
**Lines:** 206
**Avg Complexity:** 4.0


## Description

tests.signals
~~~~~~~~~~~~~~~~~~~~~~~

Signalling.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `pytest`

- `flask`

- `blinker`



## Functions


### `test_template_rendered(app, client) → None`



- **Line:** 25–43
- **Complexity:** 4
- **Calls:** route, connect, render_template, append, get, disconnect, len


### `index() → None`



- **Line:** 27–28
- **Complexity:** 1
- **Calls:** route, render_template


### `record(sender, template, context) → None`



- **Line:** 32–33
- **Complexity:** 1
- **Calls:** append


### `test_before_render_template() → None`



- **Line:** 46–68
- **Complexity:** 5
- **Calls:** Flask, route, connect, render_template, append, get, disconnect, len, test_client


### `index() → None`



- **Line:** 50–51
- **Complexity:** 1
- **Calls:** route, render_template


### `record(sender, template, context) → None`



- **Line:** 55–57
- **Complexity:** 1
- **Calls:** append


### `test_request_signals() → None`



- **Line:** 71–113
- **Complexity:** 3
- **Calls:** Flask, route, connect, append, get, disconnect, test_client


### `before_request_signal(sender) → None`



- **Line:** 75–76
- **Complexity:** 1
- **Calls:** append


### `after_request_signal(sender, response) → None`



- **Line:** 78–80
- **Complexity:** 1
- **Calls:** append


### `before_request_handler() → None`



- **Line:** 83–84
- **Complexity:** 1
- **Calls:** append


### `after_request_handler(response) → None`



- **Line:** 87–90
- **Complexity:** 1
- **Calls:** append


### `index() → None`



- **Line:** 93–95
- **Complexity:** 1
- **Calls:** route, append


### `test_request_exception_signal() → None`



- **Line:** 116–133
- **Complexity:** 4
- **Calls:** Flask, route, connect, append, isinstance, disconnect, len, get, test_client


### `index() → None`



- **Line:** 121–122
- **Complexity:** 1
- **Calls:** route


### `record(sender, exception) → None`



- **Line:** 124–125
- **Complexity:** 1
- **Calls:** append


### `test_appcontext_signals() → None`



- **Line:** 136–160
- **Complexity:** 4
- **Calls:** Flask, route, connect, append, disconnect, test_client, get


### `record_push(sender) → None`



- **Line:** 140–141
- **Complexity:** 1
- **Calls:** append


### `record_pop(sender) → None`



- **Line:** 143–144
- **Complexity:** 1
- **Calls:** append


### `index() → None`



- **Line:** 147–148
- **Complexity:** 1
- **Calls:** route


### `test_flash_signal(app) → None`



- **Line:** 163–184
- **Complexity:** 4
- **Calls:** route, connect, flash, redirect, append, test_client, disconnect, session_transaction, get, len


### `index() → None`



- **Line:** 165–167
- **Complexity:** 1
- **Calls:** route, flash, redirect


### `record(sender, message, category) → None`



- **Line:** 171–172
- **Complexity:** 1
- **Calls:** append


### `test_appcontext_tearing_down_signal() → None`



- **Line:** 187–206
- **Complexity:** 4
- **Calls:** Flask, route, connect, append, disconnect, test_client, get


### `record_teardown(sender) → None`



- **Line:** 191–192
- **Complexity:** 1
- **Calls:** append


### `index() → None`



- **Line:** 195–196
- **Complexity:** 1
- **Calls:** route



## Classes

