# Module: `tests/test_testing.py`

**Path:** `C:\temp\flask\tests\test_testing.py`
**Lines:** 447
**Avg Complexity:** 3.9


## Description

tests.testing
~~~~~~~~~~~~~

Test client and more.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `click`

- `pytest`

- `werkzeug`

- `flask`

- `flask.appcontext_popped`

- `flask._compat.text_type`

- `flask.cli.ScriptInfo`

- `flask.json.jsonify`

- `flask.testing.EnvironBuilder`

- `flask.testing.FlaskCliRunner`

- `flask.testing.make_test_environ_builder`

- `blinker`



## Functions


### `test_environ_defaults_from_config(app, client) → None`



- **Line:** 30–42
- **Complexity:** 3
- **Calls:** route, test_request_context, get


### `index() → None`



- **Line:** 35–36
- **Complexity:** 1
- **Calls:** route


### `test_environ_defaults(app, client, app_ctx, req_ctx) → None`



- **Line:** 45–54
- **Complexity:** 3
- **Calls:** route, test_request_context, get


### `index() → None`



- **Line:** 47–48
- **Complexity:** 1
- **Calls:** route


### `test_environ_base_default(app, client, app_ctx) → None`



- **Line:** 57–65
- **Complexity:** 3
- **Calls:** route, get


### `index() → None`



- **Line:** 59–61
- **Complexity:** 1
- **Calls:** route


### `test_environ_base_modified(app, client, app_ctx) → None`



- **Line:** 68–84
- **Complexity:** 5
- **Calls:** route, get


### `index() → None`



- **Line:** 70–72
- **Complexity:** 1
- **Calls:** route


### `test_client_open_environ(app, client, request) → None`



- **Line:** 87–101
- **Complexity:** 3
- **Calls:** route, EnvironBuilder, addfinalizer, open, get_environ


### `index() → None`



- **Line:** 89–90
- **Complexity:** 1
- **Calls:** route


### `test_specify_url_scheme(app, client) → None`



- **Line:** 104–113
- **Complexity:** 3
- **Calls:** route, test_request_context, get


### `index() → None`



- **Line:** 106–107
- **Complexity:** 1
- **Calls:** route


### `test_path_is_url(app) → None`



- **Line:** 116–121
- **Complexity:** 5
- **Calls:** EnvironBuilder


### `test_make_test_environ_builder(app) → None`



- **Line:** 124–130
- **Complexity:** 5
- **Calls:** deprecated_call, make_test_environ_builder


### `test_environbuilder_json_dumps(app) → None`


EnvironBuilder.json_dumps() takes settings from the app.


- **Line:** 133–137
- **Complexity:** 2
- **Calls:** EnvironBuilder, decode, read


### `test_blueprint_with_subdomain() → None`



- **Line:** 140–161
- **Complexity:** 4
- **Calls:** Flask, test_client, Blueprint, route, register_blueprint, test_request_context, get


### `index() → None`



- **Line:** 149–150
- **Complexity:** 1
- **Calls:** route


### `test_redirect_keep_session(app, client, app_ctx) → None`



- **Line:** 164–191
- **Complexity:** 8
- **Calls:** route, get, post, redirect, hasattr


### `index() → None`



- **Line:** 166–170
- **Complexity:** 1
- **Calls:** route, redirect


### `get_session() → None`



- **Line:** 173–174
- **Complexity:** 1
- **Calls:** route, get


### `test_session_transactions(app, client) → None`



- **Line:** 194–208
- **Complexity:** 6
- **Calls:** route, text_type, get, session_transaction, len


### `index() → None`



- **Line:** 196–197
- **Complexity:** 1
- **Calls:** route, text_type


### `test_session_transactions_no_null_sessions() → None`



- **Line:** 211–219
- **Complexity:** 2
- **Calls:** Flask, test_client, raises, str, session_transaction


### `test_session_transactions_keep_context(app, client, req_ctx) → None`



- **Line:** 222–227
- **Complexity:** 3
- **Calls:** get, _get_current_object, session_transaction


### `test_session_transaction_needs_cookies(app) → None`



- **Line:** 230–235
- **Complexity:** 2
- **Calls:** test_client, raises, str, session_transaction


### `test_test_client_context_binding(app, client) → None`



- **Line:** 238–267
- **Complexity:** 9
- **Calls:** route, get, AssertionError, hasattr


### `index() → None`



- **Line:** 242–244
- **Complexity:** 1
- **Calls:** route


### `other() → None`



- **Line:** 247–248
- **Complexity:** 1
- **Calls:** route


### `test_reuse_client(client) → None`



- **Line:** 270–277
- **Complexity:** 3
- **Calls:** get


### `test_test_client_calls_teardown_handlers(app, client) → None`



- **Line:** 280–300
- **Complexity:** 8
- **Calls:** append, get


### `remember(error) → None`



- **Line:** 284–285
- **Complexity:** 1
- **Calls:** append


### `test_full_url_request(app, client) → None`



- **Line:** 303–312
- **Complexity:** 4
- **Calls:** route, post


### `action() → None`



- **Line:** 305–306
- **Complexity:** 1
- **Calls:** route


### `test_json_request_and_response(app, client) → None`



- **Line:** 315–331
- **Complexity:** 6
- **Calls:** route, jsonify, post, get_json


### `echo() → None`



- **Line:** 317–318
- **Complexity:** 1
- **Calls:** route, jsonify, get_json


### `test_client_json_no_app_context(app, client) → None`



- **Line:** 335–352
- **Complexity:** 3
- **Calls:** skipif, route, Namespace, format, connected_to, post, get_data


### `hello() → None`



- **Line:** 337–338
- **Complexity:** 1
- **Calls:** route, format


### `add(self, app) → None`



- **Line:** 343–344
- **Complexity:** 1
- **Calls:** none


### `test_subdomain() → None`



- **Line:** 355–371
- **Complexity:** 3
- **Calls:** Flask, test_client, route, test_request_context, url_for, get


### `view(company_id) → None`



- **Line:** 361–362
- **Complexity:** 1
- **Calls:** route


### `test_nosubdomain(app, client) → None`



- **Line:** 374–388
- **Complexity:** 3
- **Calls:** route, test_request_context, url_for, get


### `view(company_id) → None`



- **Line:** 378–379
- **Complexity:** 1
- **Calls:** route


### `test_cli_runner_class(app) → None`



- **Line:** 391–400
- **Complexity:** 3
- **Calls:** test_cli_runner, isinstance


### `test_cli_invoke(app) → None`



- **Line:** 403–414
- **Complexity:** 3
- **Calls:** command, test_cli_runner, invoke, echo


### `hello_command() → None`



- **Line:** 405–406
- **Complexity:** 1
- **Calls:** command, echo


### `test_cli_custom_obj(app) → None`



- **Line:** 417–432
- **Complexity:** 2
- **Calls:** command, ScriptInfo, test_cli_runner, invoke, echo


### `create_app() → None`



- **Line:** 421–423
- **Complexity:** 1
- **Calls:** none


### `hello_command() → None`



- **Line:** 426–427
- **Complexity:** 1
- **Calls:** command, echo


### `test_client_pop_all_preserved(app, req_ctx, client) → None`



- **Line:** 435–447
- **Complexity:** 2
- **Calls:** route, Response, get, stream_with_context


### `index() → None`



- **Line:** 437–439
- **Complexity:** 1
- **Calls:** route, Response, stream_with_context



## Classes


### `Namespace`



- **Bases:** object
- **Methods:** add


### `SubRunner`



- **Bases:** FlaskCliRunner
- **Methods:** none


### `NS`



- **Bases:** object
- **Methods:** none

