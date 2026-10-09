# Module: `tests/test_user_error_handler.py`

**Path:** `C:\temp\flask\tests\test_user_error_handler.py`
**Lines:** 289
**Avg Complexity:** 3.8


## Description

tests.test_user_error_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `pytest`

- `werkzeug.exceptions.Forbidden`

- `werkzeug.exceptions.HTTPException`

- `werkzeug.exceptions.InternalServerError`

- `werkzeug.exceptions.NotFound`

- `flask`



## Functions


### `test_error_handler_no_match(app, client) → None`



- **Line:** 18–52
- **Complexity:** 4
- **Calls:** errorhandler, route, isinstance, getattr, CustomException, KeyError, abort, get, type


### `custom_exception_handler(e) → None`



- **Line:** 23–25
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `handle_500(e) → None`



- **Line:** 28–35
- **Complexity:** 1
- **Calls:** errorhandler, isinstance, getattr, type


### `custom_test() → None`



- **Line:** 38–39
- **Complexity:** 1
- **Calls:** route, CustomException


### `key_error() → None`



- **Line:** 42–43
- **Complexity:** 1
- **Calls:** route, KeyError


### `do_abort() → None`



- **Line:** 46–47
- **Complexity:** 1
- **Calls:** route, abort


### `test_error_handler_subclass(app) → None`



- **Line:** 55–91
- **Complexity:** 4
- **Calls:** errorhandler, route, test_client, isinstance, ParentException, ChildExceptionUnregistered, ChildExceptionRegistered, get


### `parent_exception_handler(e) → None`



- **Line:** 66–68
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `child_exception_handler(e) → None`



- **Line:** 71–73
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `parent_test() → None`



- **Line:** 76–77
- **Complexity:** 1
- **Calls:** route, ParentException


### `unregistered_test() → None`



- **Line:** 80–81
- **Complexity:** 1
- **Calls:** route, ChildExceptionUnregistered


### `registered_test() → None`



- **Line:** 84–85
- **Complexity:** 1
- **Calls:** route, ChildExceptionRegistered


### `test_error_handler_http_subclass(app) → None`



- **Line:** 94–127
- **Complexity:** 4
- **Calls:** errorhandler, route, test_client, isinstance, Forbidden, ForbiddenSubclassRegistered, ForbiddenSubclassUnregistered, get


### `code_exception_handler(e) → None`



- **Line:** 102–104
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `subclass_exception_handler(e) → None`



- **Line:** 107–109
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `forbidden_test() → None`



- **Line:** 112–113
- **Complexity:** 1
- **Calls:** route, Forbidden


### `registered_test() → None`



- **Line:** 116–117
- **Complexity:** 1
- **Calls:** route, ForbiddenSubclassRegistered


### `unregistered_test() → None`



- **Line:** 120–121
- **Complexity:** 1
- **Calls:** route, ForbiddenSubclassUnregistered


### `test_error_handler_blueprint(app) → None`



- **Line:** 130–154
- **Complexity:** 3
- **Calls:** Blueprint, errorhandler, route, register_blueprint, test_client, InternalServerError, get


### `bp_exception_handler(e) → None`



- **Line:** 134–135
- **Complexity:** 1
- **Calls:** errorhandler


### `bp_test() → None`



- **Line:** 138–139
- **Complexity:** 1
- **Calls:** route, InternalServerError


### `app_exception_handler(e) → None`



- **Line:** 142–143
- **Complexity:** 1
- **Calls:** errorhandler


### `app_test() → None`



- **Line:** 146–147
- **Complexity:** 1
- **Calls:** route, InternalServerError


### `test_default_error_handler() → None`



- **Line:** 157–208
- **Complexity:** 6
- **Calls:** Blueprint, errorhandler, route, Flask, register_blueprint, test_client, isinstance, NotFound, Forbidden, get


### `bp_exception_handler(e) → None`



- **Line:** 161–164
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `bp_forbidden_handler(e) → None`



- **Line:** 167–169
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `bp_registered_test() → None`



- **Line:** 172–173
- **Complexity:** 1
- **Calls:** route, NotFound


### `bp_forbidden_test() → None`



- **Line:** 176–177
- **Complexity:** 1
- **Calls:** route, Forbidden


### `catchall_exception_handler(e) → None`



- **Line:** 182–185
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `catchall_forbidden_handler(e) → None`



- **Line:** 188–190
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `forbidden() → None`



- **Line:** 193–194
- **Complexity:** 1
- **Calls:** route, Forbidden


### `slash() → None`



- **Line:** 197–198
- **Complexity:** 1
- **Calls:** route


### `app(self, app) → None`



- **Line:** 218–236
- **Complexity:** 1
- **Calls:** fixture, route, Custom, KeyError, abort, InternalServerError


### `do_custom() → None`



- **Line:** 220–221
- **Complexity:** 1
- **Calls:** route, Custom


### `do_error() → None`



- **Line:** 224–225
- **Complexity:** 1
- **Calls:** route, KeyError


### `do_abort() → None`



- **Line:** 228–229
- **Complexity:** 1
- **Calls:** route, abort


### `do_raise() → None`



- **Line:** 232–233
- **Complexity:** 1
- **Calls:** route, InternalServerError


### `report_error(self, e) → None`



- **Line:** 238–244
- **Complexity:** 2
- **Calls:** getattr, type


### `test_handle_class_or_code(self, app, client, to_handle) → None`


``InternalServerError`` and ``500`` are aliases, they should
have the same behavior. Both should only receive
``InternalServerError``, which might wrap another error.


- **Line:** 247–261
- **Complexity:** 5
- **Calls:** parametrize, errorhandler, isinstance, report_error, get


### `handle_500(e) → None`



- **Line:** 254–256
- **Complexity:** 1
- **Calls:** errorhandler, isinstance, report_error


### `test_handle_generic_http(self, app, client) → None`


``HTTPException`` should only receive ``HTTPException``
subclasses. It will receive ``404`` routing exceptions.


- **Line:** 263–275
- **Complexity:** 4
- **Calls:** errorhandler, isinstance, str, get


### `handle_http(e) → None`



- **Line:** 269–271
- **Complexity:** 1
- **Calls:** errorhandler, isinstance, str


### `test_handle_generic(self, app, client) → None`


Generic ``Exception`` will handle all exceptions directly,
including ``HTTPExceptions``.


- **Line:** 277–289
- **Complexity:** 5
- **Calls:** errorhandler, report_error, get


### `handle_exception(e) → None`



- **Line:** 283–284
- **Complexity:** 1
- **Calls:** errorhandler, report_error



## Classes


### `CustomException`



- **Bases:** Exception
- **Methods:** none


### `ParentException`



- **Bases:** Exception
- **Methods:** none


### `ChildExceptionUnregistered`



- **Bases:** ParentException
- **Methods:** none


### `ChildExceptionRegistered`



- **Bases:** ParentException
- **Methods:** none


### `ForbiddenSubclassRegistered`



- **Bases:** Forbidden
- **Methods:** none


### `ForbiddenSubclassUnregistered`



- **Bases:** Forbidden
- **Methods:** none


### `TestGenericHandlers`


Test how very generic handlers are dispatched to.


- **Bases:** object
- **Methods:** app, report_error, test_handle_class_or_code, test_handle_generic_http, test_handle_generic


### `Custom`



- **Bases:** Exception
- **Methods:** none

