# Module: `src/flask/signals.py`

**Path:** `C:\temp\flask\src\flask\signals.py`
**Lines:** 65
**Avg Complexity:** 1.3


## Description

flask.signals
~~~~~~~~~~~~~

Implements signals based on blinker if available, otherwise
falls silently back to a noop.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `blinker.Namespace`



## Functions


### `signal(self, name, doc) → None`



- **Line:** 20–21
- **Complexity:** 1
- **Calls:** _FakeSignal


### `__init__(self, name, doc) → None`



- **Line:** 30–32
- **Complexity:** 1
- **Calls:** none


### `send(self) → None`



- **Line:** 34–35
- **Complexity:** 1
- **Calls:** none


### `_fail(self) → None`



- **Line:** 37–41
- **Complexity:** 1
- **Calls:** RuntimeError



## Classes


### `Namespace`



- **Bases:** object
- **Methods:** signal


### `_FakeSignal`


If blinker is unavailable, create a fake class with the same
interface that allows sending of signals but will fail with an
error on anything else.  Instead of doing anything on send, it
will just ignore the arguments and do nothing instead.


- **Bases:** object
- **Methods:** __init__, send, _fail

