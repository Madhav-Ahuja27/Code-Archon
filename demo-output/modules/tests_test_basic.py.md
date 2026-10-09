# Module: `tests/test_basic.py`

**Path:** `C:\temp\flask\tests\test_basic.py`
**Lines:** 1987
**Avg Complexity:** 3.9


## Description

tests.basic
~~~~~~~~~~~~~~~~~~~~~

The basic functionality.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `re`

- `sys`

- `time`

- `uuid`

- `datetime.datetime`

- `threading.Thread`

- `pytest`

- `werkzeug.serving`

- `werkzeug.exceptions.BadRequest`

- `werkzeug.exceptions.Forbidden`

- `werkzeug.exceptions.NotFound`

- `werkzeug.http.parse_date`

- `werkzeug.routing.BuildError`

- `flask`

- `flask._compat.text_type`

- `werkzeug.routing.Submount`

- `werkzeug.routing.Rule`

- `werkzeug.routing.Submount`

- `werkzeug.routing.Rule`

- `flask.debughelpers.DebugFilesKeyError`

- `dataclasses.make_dataclass`

- `pathlib.Path`



## Functions


### `test_options_work(app, client) → None`



- **Line:** 30–37
- **Complexity:** 3
- **Calls:** route, open, sorted


### `index() → None`



- **Line:** 32–33
- **Complexity:** 1
- **Calls:** route


### `test_options_on_multiple_rules(app, client) → None`



- **Line:** 40–50
- **Complexity:** 2
- **Calls:** route, open, sorted


### `index() → None`



- **Line:** 42–43
- **Complexity:** 1
- **Calls:** route


### `index_put() → None`



- **Line:** 46–47
- **Complexity:** 1
- **Calls:** route


### `test_provide_automatic_options_attr() → None`



- **Line:** 53–72
- **Complexity:** 3
- **Calls:** Flask, open, route, sorted, test_client


### `index() → None`



- **Line:** 56–57
- **Complexity:** 1
- **Calls:** none


### `index2() → None`



- **Line:** 66–67
- **Complexity:** 1
- **Calls:** none


### `test_provide_automatic_options_kwarg(app, client) → None`



- **Line:** 75–118
- **Complexity:** 14
- **Calls:** add_url_rule, post, hasattr, head, delete, sorted, options, open, get


### `index() → None`



- **Line:** 76–77
- **Complexity:** 1
- **Calls:** none


### `more() → None`



- **Line:** 79–80
- **Complexity:** 1
- **Calls:** none


### `test_request_dispatching(app, client) → None`



- **Line:** 121–141
- **Complexity:** 10
- **Calls:** route, post, head, delete, sorted, get


### `index() → None`



- **Line:** 123–124
- **Complexity:** 1
- **Calls:** route


### `more() → None`



- **Line:** 127–128
- **Complexity:** 1
- **Calls:** route


### `test_disallow_string_for_allowed_methods(app) → None`



- **Line:** 144–149
- **Complexity:** 1
- **Calls:** raises, route


### `index() → None`



- **Line:** 148–149
- **Complexity:** 1
- **Calls:** route


### `test_url_mapping(app, client) → None`



- **Line:** 152–185
- **Complexity:** 12
- **Calls:** add_url_rule, post, head, delete, open, sorted, decode, get


### `index() → None`



- **Line:** 155–156
- **Complexity:** 1
- **Calls:** none


### `more() → None`



- **Line:** 158–159
- **Complexity:** 1
- **Calls:** none


### `options() → None`



- **Line:** 161–162
- **Complexity:** 1
- **Calls:** none


### `test_werkzeug_routing(app, client) → None`



- **Line:** 188–205
- **Complexity:** 3
- **Calls:** add, Submount, get, Rule


### `bar() → None`



- **Line:** 195–196
- **Complexity:** 1
- **Calls:** none


### `index() → None`



- **Line:** 198–199
- **Complexity:** 1
- **Calls:** none


### `test_endpoint_decorator(app, client) → None`



- **Line:** 208–224
- **Complexity:** 3
- **Calls:** add, endpoint, Submount, get, Rule


### `bar() → None`



- **Line:** 216–217
- **Complexity:** 1
- **Calls:** endpoint


### `index() → None`



- **Line:** 220–221
- **Complexity:** 1
- **Calls:** endpoint


### `test_session(app, client) → None`



- **Line:** 227–247
- **Complexity:** 3
- **Calls:** route, get, post


### `set() → None`



- **Line:** 229–235
- **Complexity:** 1
- **Calls:** route


### `get() → None`



- **Line:** 238–244
- **Complexity:** 1
- **Calls:** route, get


### `test_session_using_server_name(app, client) → None`



- **Line:** 250–260
- **Complexity:** 3
- **Calls:** update, route, get, lower


### `index() → None`



- **Line:** 254–256
- **Complexity:** 1
- **Calls:** route


### `test_session_using_server_name_and_port(app, client) → None`



- **Line:** 263–273
- **Complexity:** 3
- **Calls:** update, route, get, lower


### `index() → None`



- **Line:** 267–269
- **Complexity:** 1
- **Calls:** route


### `test_session_using_server_name_port_and_path(app, client) → None`



- **Line:** 276–287
- **Complexity:** 4
- **Calls:** update, route, get, lower


### `index() → None`



- **Line:** 280–282
- **Complexity:** 1
- **Calls:** route


### `test_session_using_application_root(app, client) → None`



- **Line:** 290–309
- **Complexity:** 2
- **Calls:** PrefixPathMiddleware, update, route, get, lower, app


### `__init__(self, app, prefix) → None`



- **Line:** 292–294
- **Complexity:** 1
- **Calls:** none


### `__call__(self, environ, start_response) → None`



- **Line:** 296–298
- **Complexity:** 1
- **Calls:** app


### `index() → None`



- **Line:** 304–306
- **Complexity:** 1
- **Calls:** route


### `test_session_using_session_settings(app, client) → None`



- **Line:** 312–334
- **Complexity:** 6
- **Calls:** update, route, get, lower


### `index() → None`



- **Line:** 324–326
- **Complexity:** 1
- **Calls:** route


### `test_session_using_samesite_attribute(app, client) → None`



- **Line:** 337–361
- **Complexity:** 4
- **Calls:** route, update, get, lower, raises


### `index() → None`



- **Line:** 339–341
- **Complexity:** 1
- **Calls:** route


### `test_session_localhost_warning(recwarn, app, client) → None`



- **Line:** 364–375
- **Complexity:** 3
- **Calls:** update, route, get, pop, lower, str


### `index() → None`



- **Line:** 368–370
- **Complexity:** 1
- **Calls:** route


### `test_session_ip_warning(recwarn, app, client) → None`



- **Line:** 378–389
- **Complexity:** 3
- **Calls:** update, route, get, pop, lower, str


### `index() → None`



- **Line:** 382–384
- **Complexity:** 1
- **Calls:** route


### `test_missing_session(app) → None`



- **Line:** 392–402
- **Complexity:** 2
- **Calls:** raises, test_request_context, expect_exception, get


### `expect_exception(f) → None`



- **Line:** 395–397
- **Complexity:** 1
- **Calls:** raises


### `test_session_expiration(app, client) → None`



- **Line:** 405–434
- **Complexity:** 8
- **Calls:** route, get, search, parse_date, text_type, group, utcnow


### `index() → None`



- **Line:** 409–412
- **Complexity:** 1
- **Calls:** route


### `test() → None`



- **Line:** 415–416
- **Complexity:** 1
- **Calls:** route, text_type


### `test_session_stored_last(app, client) → None`



- **Line:** 437–448
- **Complexity:** 3
- **Calls:** route, repr, get


### `modify_session(response) → None`



- **Line:** 439–441
- **Complexity:** 1
- **Calls:** none


### `dump_session_contents() → None`



- **Line:** 444–445
- **Complexity:** 1
- **Calls:** route, repr, get


### `test_session_special_types(app, client) → None`



- **Line:** 451–479
- **Complexity:** 11
- **Calls:** replace, uuid4, route, Markup, get, utcnow, type


### `dump_session_contents() → None`



- **Line:** 456–465
- **Complexity:** 1
- **Calls:** route, Markup


### `test_session_cookie_setting(app) → None`



- **Line:** 482–520
- **Complexity:** 1
- **Calls:** route, run_test, str, get, test_client


### `bump() → None`



- **Line:** 486–489
- **Complexity:** 1
- **Calls:** route, str, get


### `read() → None`



- **Line:** 492–493
- **Complexity:** 1
- **Calls:** route, str, get


### `run_test(expect_header) → None`



- **Line:** 495–504
- **Complexity:** 1
- **Calls:** test_client, get


### `test_session_vary_cookie(app, client) → None`



- **Line:** 523–575
- **Complexity:** 1
- **Calls:** route, expect, get, setdefault, Response, add, update, len, get_all


### `set_session() → None`



- **Line:** 525–527
- **Complexity:** 1
- **Calls:** route


### `get() → None`



- **Line:** 530–531
- **Complexity:** 1
- **Calls:** route, get


### `getitem() → None`



- **Line:** 534–535
- **Complexity:** 1
- **Calls:** route


### `setdefault() → None`



- **Line:** 538–539
- **Complexity:** 1
- **Calls:** route, setdefault


### `vary_cookie_header_set() → None`



- **Line:** 542–546
- **Complexity:** 1
- **Calls:** route, Response, add


### `vary_header_set() → None`



- **Line:** 549–553
- **Complexity:** 1
- **Calls:** route, Response, update


### `no_vary_header() → None`



- **Line:** 556–557
- **Complexity:** 1
- **Calls:** route


### `expect(path, header_value) → None`



- **Line:** 559–567
- **Complexity:** 1
- **Calls:** get, len, get_all


### `test_flashes(app, req_ctx) → None`



- **Line:** 578–584
- **Complexity:** 4
- **Calls:** flash, list, get_flashed_messages


### `test_extended_flashing(app) → None`



- **Line:** 587–665
- **Complexity:** 1
- **Calls:** route, test_client, get, flash, get_flashed_messages, Markup, list, len


### `index() → None`



- **Line:** 595–599
- **Complexity:** 1
- **Calls:** route, flash, Markup


### `test() → None`



- **Line:** 602–609
- **Complexity:** 1
- **Calls:** route, get_flashed_messages, list, Markup


### `test_with_categories() → None`



- **Line:** 612–620
- **Complexity:** 1
- **Calls:** route, get_flashed_messages, len, list, Markup


### `test_filter() → None`



- **Line:** 623–628
- **Complexity:** 1
- **Calls:** route, get_flashed_messages, list


### `test_filters() → None`



- **Line:** 631–639
- **Complexity:** 1
- **Calls:** route, get_flashed_messages, list, Markup


### `test_filters2() → None`



- **Line:** 642–647
- **Complexity:** 1
- **Calls:** route, get_flashed_messages, len, Markup


### `test_request_processing(app, client) → None`



- **Line:** 668–690
- **Complexity:** 4
- **Calls:** route, append, get


### `before_request() → None`



- **Line:** 672–673
- **Complexity:** 1
- **Calls:** append


### `after_request(response) → None`



- **Line:** 676–679
- **Complexity:** 1
- **Calls:** append


### `index() → None`



- **Line:** 682–685
- **Complexity:** 1
- **Calls:** route


### `test_request_preprocessing_early_return(app, client) → None`



- **Line:** 693–717
- **Complexity:** 3
- **Calls:** route, strip, append, get


### `before_request1() → None`



- **Line:** 697–698
- **Complexity:** 1
- **Calls:** append


### `before_request2() → None`



- **Line:** 701–703
- **Complexity:** 1
- **Calls:** append


### `before_request3() → None`



- **Line:** 706–708
- **Complexity:** 1
- **Calls:** append


### `index() → None`



- **Line:** 711–713
- **Complexity:** 1
- **Calls:** route, append


### `test_after_request_processing(app, client) → None`



- **Line:** 720–732
- **Complexity:** 3
- **Calls:** route, get


### `index() → None`



- **Line:** 722–728
- **Complexity:** 1
- **Calls:** route


### `foo(response) → None`



- **Line:** 724–726
- **Complexity:** 1
- **Calls:** none


### `test_teardown_request_handler(app, client) → None`



- **Line:** 735–750
- **Complexity:** 4
- **Calls:** route, get, append, len


### `teardown_request(exc) → None`



- **Line:** 739–741
- **Complexity:** 1
- **Calls:** append


### `root() → None`



- **Line:** 744–745
- **Complexity:** 1
- **Calls:** route


### `test_teardown_request_handler_debug_mode(app, client) → None`



- **Line:** 753–768
- **Complexity:** 4
- **Calls:** route, get, append, len


### `teardown_request(exc) → None`



- **Line:** 757–759
- **Complexity:** 1
- **Calls:** append


### `root() → None`



- **Line:** 762–763
- **Complexity:** 1
- **Calls:** route


### `test_teardown_request_handler_error(app, client) → None`



- **Line:** 771–806
- **Complexity:** 4
- **Calls:** route, get, append, len, type, TypeError


### `teardown_request1(exc) → None`



- **Line:** 776–785
- **Complexity:** 1
- **Calls:** append, type, TypeError


### `teardown_request2(exc) → None`



- **Line:** 788–797
- **Complexity:** 1
- **Calls:** append, type, TypeError


### `fails() → None`



- **Line:** 800–801
- **Complexity:** 1
- **Calls:** route


### `test_before_after_request_order(app, client) → None`



- **Line:** 809–844
- **Complexity:** 3
- **Calls:** route, get, append


### `before1() → None`



- **Line:** 813–814
- **Complexity:** 1
- **Calls:** append


### `before2() → None`



- **Line:** 817–818
- **Complexity:** 1
- **Calls:** append


### `after1(response) → None`



- **Line:** 821–823
- **Complexity:** 1
- **Calls:** append


### `after2(response) → None`



- **Line:** 826–828
- **Complexity:** 1
- **Calls:** append


### `finish1(exc) → None`



- **Line:** 831–832
- **Complexity:** 1
- **Calls:** append


### `finish2(exc) → None`



- **Line:** 835–836
- **Complexity:** 1
- **Calls:** append


### `index() → None`



- **Line:** 839–840
- **Complexity:** 1
- **Calls:** route


### `test_error_handling(app, client) → None`



- **Line:** 847–882
- **Complexity:** 7
- **Calls:** errorhandler, route, get, abort


### `not_found(e) → None`



- **Line:** 851–852
- **Complexity:** 1
- **Calls:** errorhandler


### `internal_server_error(e) → None`



- **Line:** 855–856
- **Complexity:** 1
- **Calls:** errorhandler


### `forbidden(e) → None`



- **Line:** 859–860
- **Complexity:** 1
- **Calls:** errorhandler


### `index() → None`



- **Line:** 863–864
- **Complexity:** 1
- **Calls:** route, abort


### `error() → None`



- **Line:** 867–868
- **Complexity:** 1
- **Calls:** route


### `error2() → None`



- **Line:** 871–872
- **Complexity:** 1
- **Calls:** route, abort


### `test_error_handler_unknown_code(app) → None`



- **Line:** 885–889
- **Complexity:** 2
- **Calls:** raises, register_error_handler


### `test_error_handling_processing(app, client) → None`



- **Line:** 892–910
- **Complexity:** 3
- **Calls:** errorhandler, route, get


### `internal_server_error(e) → None`



- **Line:** 896–897
- **Complexity:** 1
- **Calls:** errorhandler


### `broken_func() → None`



- **Line:** 900–901
- **Complexity:** 1
- **Calls:** route


### `after_request(resp) → None`



- **Line:** 904–906
- **Complexity:** 1
- **Calls:** none


### `test_baseexception_error_handling(app, client) → None`



- **Line:** 913–925
- **Complexity:** 3
- **Calls:** route, KeyboardInterrupt, raises, get, type


### `broken_func() → None`



- **Line:** 917–918
- **Complexity:** 1
- **Calls:** route, KeyboardInterrupt


### `test_before_request_and_routing_errors(app, client) → None`



- **Line:** 928–939
- **Complexity:** 3
- **Calls:** errorhandler, get


### `attach_something() → None`



- **Line:** 930–931
- **Complexity:** 1
- **Calls:** none


### `return_something(error) → None`



- **Line:** 934–935
- **Complexity:** 1
- **Calls:** errorhandler


### `test_user_error_handling(app, client) → None`



- **Line:** 942–955
- **Complexity:** 2
- **Calls:** errorhandler, route, isinstance, MyException, get


### `handle_my_exception(e) → None`



- **Line:** 947–949
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `index() → None`



- **Line:** 952–953
- **Complexity:** 1
- **Calls:** route, MyException


### `test_http_error_subclass_handling(app, client) → None`



- **Line:** 958–987
- **Complexity:** 4
- **Calls:** errorhandler, route, isinstance, ForbiddenSubclass, abort, Forbidden, get


### `handle_forbidden_subclass(e) → None`



- **Line:** 963–965
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `handle_403(e) → None`



- **Line:** 968–971
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `index1() → None`



- **Line:** 974–975
- **Complexity:** 1
- **Calls:** route, ForbiddenSubclass


### `index2() → None`



- **Line:** 978–979
- **Complexity:** 1
- **Calls:** route, abort


### `index3() → None`



- **Line:** 982–983
- **Complexity:** 1
- **Calls:** route, Forbidden


### `test_errorhandler_precedence(app, client) → None`



- **Line:** 990–1020
- **Complexity:** 3
- **Calls:** errorhandler, route, get


### `handle_e2(e) → None`



- **Line:** 1001–1002
- **Complexity:** 1
- **Calls:** errorhandler


### `handle_exception(e) → None`



- **Line:** 1005–1006
- **Complexity:** 1
- **Calls:** errorhandler


### `raise_e1() → None`



- **Line:** 1009–1010
- **Complexity:** 1
- **Calls:** route


### `raise_e3() → None`



- **Line:** 1013–1014
- **Complexity:** 1
- **Calls:** route


### `test_trapping_of_bad_request_key_errors(app, client) → None`



- **Line:** 1023–1051
- **Complexity:** 7
- **Calls:** route, get, errisinstance, abort, raises, get_description


### `fail() → None`



- **Line:** 1025–1026
- **Complexity:** 1
- **Calls:** route


### `allow_abort() → None`



- **Line:** 1029–1030
- **Complexity:** 1
- **Calls:** route, abort


### `test_trapping_of_all_http_exceptions(app, client) → None`



- **Line:** 1054–1062
- **Complexity:** 1
- **Calls:** route, abort, raises, get


### `fail() → None`



- **Line:** 1058–1059
- **Complexity:** 1
- **Calls:** route, abort


### `test_error_handler_after_processor_error(app, client) → None`



- **Line:** 1065–1090
- **Complexity:** 4
- **Calls:** route, errorhandler, get


### `before_request() → None`



- **Line:** 1069–1071
- **Complexity:** 1
- **Calls:** none


### `after_request(response) → None`



- **Line:** 1074–1077
- **Complexity:** 1
- **Calls:** none


### `index() → None`



- **Line:** 1080–1081
- **Complexity:** 1
- **Calls:** route


### `internal_server_error(e) → None`



- **Line:** 1084–1085
- **Complexity:** 1
- **Calls:** errorhandler


### `test_enctype_debug_helper(app, client) → None`



- **Line:** 1093–1109
- **Complexity:** 3
- **Calls:** route, raises, post, str


### `index() → None`



- **Line:** 1099–1100
- **Complexity:** 1
- **Calls:** route


### `test_response_types(app, client) → None`



- **Line:** 1112–1192
- **Complexity:** 24
- **Calls:** route, get, encode, NotFound, getlist, Response, response_class


### `from_text() → None`



- **Line:** 1114–1115
- **Complexity:** 1
- **Calls:** route


### `from_bytes() → None`



- **Line:** 1118–1119
- **Complexity:** 1
- **Calls:** route, encode


### `from_full_tuple() → None`



- **Line:** 1122–1127
- **Complexity:** 1
- **Calls:** route


### `from_text_headers() → None`



- **Line:** 1130–1131
- **Complexity:** 1
- **Calls:** route


### `from_text_status() → None`



- **Line:** 1134–1135
- **Complexity:** 1
- **Calls:** route


### `from_response_headers() → None`



- **Line:** 1138–1142
- **Complexity:** 1
- **Calls:** route, Response


### `from_response_status() → None`



- **Line:** 1145–1146
- **Complexity:** 1
- **Calls:** route, response_class


### `from_wsgi() → None`



- **Line:** 1149–1150
- **Complexity:** 1
- **Calls:** route, NotFound


### `from_dict() → None`



- **Line:** 1153–1154
- **Complexity:** 1
- **Calls:** route


### `test_response_type_errors() → None`



- **Line:** 1195–1235
- **Complexity:** 4
- **Calls:** Flask, route, test_client, raises, get, str


### `from_none() → None`



- **Line:** 1200–1201
- **Complexity:** 1
- **Calls:** route


### `from_small_tuple() → None`



- **Line:** 1204–1205
- **Complexity:** 1
- **Calls:** route


### `from_large_tuple() → None`



- **Line:** 1208–1209
- **Complexity:** 1
- **Calls:** route


### `from_bad_type() → None`



- **Line:** 1212–1213
- **Complexity:** 1
- **Calls:** route


### `from_bad_wsgi() → None`



- **Line:** 1216–1217
- **Complexity:** 1
- **Calls:** route


### `test_make_response(app, req_ctx) → None`



- **Line:** 1238–1252
- **Complexity:** 10
- **Calls:** make_response


### `test_make_response_with_response_instance(app, req_ctx) → None`



- **Line:** 1255–1273
- **Complexity:** 10
- **Calls:** make_response, jsonify, Response


### `test_jsonify_no_prettyprint(app, req_ctx) → None`



- **Line:** 1276–1282
- **Complexity:** 2
- **Calls:** update, make_response, jsonify


### `test_jsonify_prettyprint(app, req_ctx) → None`



- **Line:** 1285–1293
- **Complexity:** 2
- **Calls:** update, make_response, jsonify


### `test_jsonify_mimetype(app, req_ctx) → None`



- **Line:** 1296–1300
- **Complexity:** 2
- **Calls:** update, make_response, jsonify


### `test_json_dump_dataclass(app, req_ctx) → None`



- **Line:** 1304–1310
- **Complexity:** 2
- **Calls:** skipif, make_dataclass, dumps, loads, Data


### `test_jsonify_args_and_kwargs_check(app, req_ctx) → None`



- **Line:** 1313–1316
- **Complexity:** 2
- **Calls:** raises, jsonify, str


### `test_url_generation(app, req_ctx) → None`



- **Line:** 1319–1328
- **Complexity:** 3
- **Calls:** route, url_for


### `hello() → None`



- **Line:** 1321–1322
- **Complexity:** 1
- **Calls:** route


### `test_build_error_handler(app) → None`



- **Line:** 1331–1354
- **Complexity:** 4
- **Calls:** append, test_request_context, raises, RuntimeError, url_for


### `handler(error, endpoint, values) → None`



- **Line:** 1348–1350
- **Complexity:** 1
- **Calls:** none


### `test_build_error_handler_reraise(app) → None`



- **Line:** 1357–1365
- **Complexity:** 1
- **Calls:** append, test_request_context, raises


### `handler_raises_build_error(error, endpoint, values) → None`



- **Line:** 1359–1360
- **Complexity:** 1
- **Calls:** none


### `test_url_for_passes_special_values_to_build_error_handler(app) → None`



- **Line:** 1368–1380
- **Complexity:** 1
- **Calls:** test_request_context, url_for


### `handler(error, endpoint, values) → None`



- **Line:** 1370–1377
- **Complexity:** 1
- **Calls:** none


### `test_static_files(app, client) → None`



- **Line:** 1383–1389
- **Complexity:** 4
- **Calls:** get, close, strip, test_request_context, url_for


### `test_static_url_path() → None`



- **Line:** 1392–1400
- **Complexity:** 3
- **Calls:** Flask, get, close, test_request_context, test_client, url_for


### `test_static_url_path_with_ending_slash() → None`



- **Line:** 1403–1411
- **Complexity:** 3
- **Calls:** Flask, get, close, test_request_context, test_client, url_for


### `test_static_url_empty_path(app) → None`



- **Line:** 1414–1418
- **Complexity:** 2
- **Calls:** Flask, open, close, test_client


### `test_static_url_empty_path_default(app) → None`



- **Line:** 1421–1425
- **Complexity:** 2
- **Calls:** Flask, open, close, test_client


### `test_static_folder_with_pathlib_path(app) → None`



- **Line:** 1428–1434
- **Complexity:** 2
- **Calls:** Flask, open, close, Path, test_client


### `test_static_folder_with_ending_slash() → None`



- **Line:** 1437–1445
- **Complexity:** 2
- **Calls:** Flask, route, get, test_client


### `catch_all(path) → None`



- **Line:** 1441–1442
- **Complexity:** 1
- **Calls:** route


### `test_static_route_with_host_matching() → None`



- **Line:** 1448–1466
- **Complexity:** 3
- **Calls:** Flask, test_client, get, close, test_request_context, url_for, raises


### `test_request_locals() → None`



- **Line:** 1469–1471
- **Complexity:** 3
- **Calls:** repr


### `test_server_name_subdomain() → None`



- **Line:** 1474–1513
- **Complexity:** 9
- **Calls:** Flask, test_client, route, get, warns


### `index() → None`



- **Line:** 1479–1480
- **Complexity:** 1
- **Calls:** route


### `subdomain() → None`



- **Line:** 1483–1484
- **Complexity:** 1
- **Calls:** route


### `test_exception_propagation(app, client) → None`



- **Line:** 1516–1536
- **Complexity:** 2
- **Calls:** route, Thread, start, join, raises, get


### `apprunner(config_key) → None`



- **Line:** 1517–1527
- **Complexity:** 1
- **Calls:** route, raises, get


### `index() → None`



- **Line:** 1519–1520
- **Complexity:** 1
- **Calls:** route


### `test_werkzeug_passthrough_errors(monkeypatch, debug, use_debugger, use_reloader, propagate_exceptions, app) → None`



- **Line:** 1543–1554
- **Complexity:** 1
- **Calls:** parametrize, setattr, run, get


### `run_simple_mock() → None`



- **Line:** 1549–1550
- **Complexity:** 1
- **Calls:** get


### `test_max_content_length(app, client) → None`



- **Line:** 1557–1575
- **Complexity:** 2
- **Calls:** route, errorhandler, post, AssertionError


### `always_first() → None`



- **Line:** 1561–1563
- **Complexity:** 1
- **Calls:** AssertionError


### `accept_file() → None`



- **Line:** 1566–1568
- **Complexity:** 1
- **Calls:** route, AssertionError


### `catcher(error) → None`



- **Line:** 1571–1572
- **Complexity:** 1
- **Calls:** errorhandler


### `test_url_processors(app, client) → None`



- **Line:** 1578–1604
- **Complexity:** 4
- **Calls:** route, pop, url_for, is_endpoint_expecting, setdefault, get


### `add_language_code(endpoint, values) → None`



- **Line:** 1580–1584
- **Complexity:** 1
- **Calls:** is_endpoint_expecting, setdefault


### `pull_lang_code(endpoint, values) → None`



- **Line:** 1587–1588
- **Complexity:** 1
- **Calls:** pop


### `index() → None`



- **Line:** 1591–1592
- **Complexity:** 1
- **Calls:** route, url_for


### `about() → None`



- **Line:** 1595–1596
- **Complexity:** 1
- **Calls:** route, url_for


### `something_else() → None`



- **Line:** 1599–1600
- **Complexity:** 1
- **Calls:** route, url_for


### `test_inject_blueprint_url_defaults(app) → None`



- **Line:** 1607–1628
- **Complexity:** 3
- **Calls:** Blueprint, route, register_blueprint, dict, inject_url_defaults, test_request_context, url_for


### `bp_defaults(endpoint, values) → None`



- **Line:** 1611–1612
- **Complexity:** 1
- **Calls:** none


### `view(page) → None`



- **Line:** 1615–1616
- **Complexity:** 1
- **Calls:** route


### `test_nonascii_pathinfo(app, client) → None`



- **Line:** 1631–1637
- **Complexity:** 2
- **Calls:** route, get


### `index() → None`



- **Line:** 1633–1634
- **Complexity:** 1
- **Calls:** route


### `test_debug_mode_complains_after_first_request(app, client) → None`



- **Line:** 1640–1664
- **Complexity:** 6
- **Calls:** route, raises, str, get


### `index() → None`



- **Line:** 1644–1645
- **Complexity:** 1
- **Calls:** route


### `broken() → None`



- **Line:** 1652–1653
- **Complexity:** 1
- **Calls:** route


### `working() → None`



- **Line:** 1660–1661
- **Complexity:** 1
- **Calls:** route


### `test_before_first_request_functions(app, client) → None`



- **Line:** 1667–1678
- **Complexity:** 4
- **Calls:** get, append


### `foo() → None`



- **Line:** 1671–1672
- **Complexity:** 1
- **Calls:** append


### `test_before_first_request_functions_concurrent(app, client) → None`



- **Line:** 1681–1697
- **Complexity:** 2
- **Calls:** Thread, start, get_and_assert, join, sleep, append, get


### `foo() → None`



- **Line:** 1685–1687
- **Complexity:** 1
- **Calls:** sleep, append


### `get_and_assert() → None`



- **Line:** 1689–1691
- **Complexity:** 1
- **Calls:** get


### `test_routing_redirect_debugging(app, client) → None`



- **Line:** 1700–1721
- **Complexity:** 5
- **Calls:** route, get, post, raises, str


### `foo() → None`



- **Line:** 1704–1705
- **Complexity:** 1
- **Calls:** route


### `test_route_decorator_custom_endpoint(app, client) → None`



- **Line:** 1724–1746
- **Complexity:** 7
- **Calls:** route, test_request_context, url_for, get


### `foo() → None`



- **Line:** 1728–1729
- **Complexity:** 1
- **Calls:** route


### `for_bar() → None`



- **Line:** 1732–1733
- **Complexity:** 1
- **Calls:** route


### `for_bar_foo() → None`



- **Line:** 1736–1737
- **Complexity:** 1
- **Calls:** route


### `test_preserve_only_once(app, client) → None`



- **Line:** 1749–1765
- **Complexity:** 6
- **Calls:** route, range, pop, raises, get


### `fail_func() → None`



- **Line:** 1753–1754
- **Complexity:** 1
- **Calls:** route


### `test_preserve_remembers_exception(app, client) → None`



- **Line:** 1768–1797
- **Complexity:** 6
- **Calls:** route, get, isinstance, append, raises, len


### `fail_func() → None`



- **Line:** 1773–1774
- **Complexity:** 1
- **Calls:** route


### `success_func() → None`



- **Line:** 1777–1778
- **Complexity:** 1
- **Calls:** route


### `teardown_handler(exc) → None`



- **Line:** 1781–1782
- **Complexity:** 1
- **Calls:** append


### `test_get_method_on_g(app_ctx) → None`



- **Line:** 1800–1805
- **Complexity:** 5
- **Calls:** get


### `test_g_iteration_protocol(app_ctx) → None`



- **Line:** 1808–1813
- **Complexity:** 4
- **Calls:** sorted


### `test_subdomain_basic_support() → None`



- **Line:** 1816–1833
- **Complexity:** 3
- **Calls:** Flask, test_client, route, get


### `normal_index() → None`



- **Line:** 1822–1823
- **Complexity:** 1
- **Calls:** route


### `test_index() → None`



- **Line:** 1826–1827
- **Complexity:** 1
- **Calls:** route


### `test_subdomain_matching() → None`



- **Line:** 1836–1846
- **Complexity:** 2
- **Calls:** Flask, test_client, route, get


### `index(user) → None`



- **Line:** 1842–1843
- **Complexity:** 1
- **Calls:** route


### `test_subdomain_matching_with_ports() → None`



- **Line:** 1849–1859
- **Complexity:** 2
- **Calls:** Flask, test_client, route, get


### `index(user) → None`



- **Line:** 1855–1856
- **Complexity:** 1
- **Calls:** route


### `test_subdomain_matching_other_name(matching) → None`



- **Line:** 1863–1880
- **Complexity:** 3
- **Calls:** parametrize, Flask, test_client, route, get, warns


### `index() → None`



- **Line:** 1869–1870
- **Complexity:** 1
- **Calls:** route


### `test_multi_route_rules(app, client) → None`



- **Line:** 1883–1892
- **Complexity:** 3
- **Calls:** route, open


### `index(test) → None`



- **Line:** 1886–1887
- **Complexity:** 1
- **Calls:** route


### `test_multi_route_class_views(app, client) → None`



- **Line:** 1895–1908
- **Complexity:** 3
- **Calls:** View, open, add_url_rule


### `__init__(self, app) → None`



- **Line:** 1897–1899
- **Complexity:** 1
- **Calls:** add_url_rule


### `index(self, test) → None`



- **Line:** 1901–1902
- **Complexity:** 1
- **Calls:** none


### `test_run_defaults(monkeypatch, app) → None`



- **Line:** 1911–1920
- **Complexity:** 2
- **Calls:** setattr, run


### `run_simple_mock() → None`



- **Line:** 1915–1916
- **Complexity:** 1
- **Calls:** none


### `test_run_server_port(monkeypatch, app) → None`



- **Line:** 1923–1933
- **Complexity:** 2
- **Calls:** setattr, run


### `run_simple_mock(hostname, port, application) → None`



- **Line:** 1927–1928
- **Complexity:** 1
- **Calls:** none


### `test_run_from_config(monkeypatch, host, port, server_name, expect_host, expect_port, app) → None`



- **Line:** 1948–1957
- **Complexity:** 1
- **Calls:** parametrize, setattr, run


### `run_simple_mock(hostname, port) → None`



- **Line:** 1951–1953
- **Complexity:** 1
- **Calls:** none


### `test_max_cookie_size(app, client, recwarn) → None`



- **Line:** 1960–1987
- **Complexity:** 6
- **Calls:** Response, route, get, pop, app_context, set_cookie, len, str


### `index() → None`



- **Line:** 1974–1977
- **Complexity:** 1
- **Calls:** route, Response, set_cookie



## Classes


### `PrefixPathMiddleware`



- **Bases:** object
- **Methods:** __init__, __call__


### `MyException`



- **Bases:** Exception
- **Methods:** none


### `ForbiddenSubclass`



- **Bases:** Forbidden
- **Methods:** none


### `E1`



- **Bases:** Exception
- **Methods:** none


### `E2`



- **Bases:** Exception
- **Methods:** none


### `E3`



- **Bases:** E1, E2
- **Methods:** none


### `View`



- **Bases:** object
- **Methods:** __init__, index

