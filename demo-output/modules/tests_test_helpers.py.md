# Module: `tests/test_helpers.py`

**Path:** `C:\temp\flask\tests\test_helpers.py`
**Lines:** 1050
**Avg Complexity:** 3.4


## Description

tests.helpers
~~~~~~~~~~~~~~~~~~~~~~~

Various helpers.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `datetime`

- `io`

- `os`

- `sys`

- `uuid`

- `pytest`

- `werkzeug.datastructures.Range`

- `werkzeug.exceptions.BadRequest`

- `werkzeug.exceptions.NotFound`

- `werkzeug.http.http_date`

- `werkzeug.http.parse_cache_control_header`

- `werkzeug.http.parse_options_header`

- `flask`

- `flask.json`

- `flask._compat.StringIO`

- `flask._compat.text_type`

- `flask.helpers.get_debug_flag`

- `flask.helpers.get_env`

- `codecs`

- `flask.views.MethodView`



## Functions


### `has_encoding(name) → None`



- **Line:** 33–40
- **Complexity:** 2
- **Calls:** lookup


### `__init__(self, path) → None`



- **Line:** 50–51
- **Complexity:** 1
- **Calls:** none


### `__fspath__(self) → None`



- **Line:** 53–54
- **Complexity:** 1
- **Calls:** none


### `__init__(self, hours, name) → None`



- **Line:** 64–66
- **Complexity:** 1
- **Calls:** timedelta


### `utcoffset(self, dt) → None`



- **Line:** 68–69
- **Complexity:** 1
- **Calls:** none


### `tzname(self, dt) → None`



- **Line:** 71–72
- **Complexity:** 1
- **Calls:** none


### `dst(self, dt) → None`



- **Line:** 74–75
- **Complexity:** 1
- **Calls:** timedelta


### `test_detect_encoding(self, value, encoding) → None`



- **Line:** 95–98
- **Complexity:** 3
- **Calls:** parametrize, encode, detect_encoding, loads, dumps


### `test_bad_request_debug_message(self, app, client, debug) → None`



- **Line:** 101–113
- **Complexity:** 3
- **Calls:** parametrize, route, post, get_json


### `post_json() → None`



- **Line:** 106–108
- **Complexity:** 1
- **Calls:** route, get_json


### `test_json_bad_requests(self, app, client) → None`



- **Line:** 115–121
- **Complexity:** 2
- **Calls:** route, post, jsonify, text_type, get_json


### `return_json() → None`



- **Line:** 117–118
- **Complexity:** 1
- **Calls:** route, jsonify, text_type, get_json


### `test_json_custom_mimetypes(self, app, client) → None`



- **Line:** 123–129
- **Complexity:** 2
- **Calls:** route, post, get_json


### `return_json() → None`



- **Line:** 125–126
- **Complexity:** 1
- **Calls:** route, get_json


### `test_json_as_unicode(self, test_value, expected, app, app_ctx) → None`



- **Line:** 134–138
- **Complexity:** 2
- **Calls:** parametrize, dumps


### `test_json_dump_to_file(self, app, app_ctx) → None`



- **Line:** 140–147
- **Complexity:** 2
- **Calls:** StringIO, dump, seek, load


### `test_jsonify_basic_types(self, test_value, app, client) → None`


Test jsonify with basic types.


- **Line:** 152–159
- **Complexity:** 3
- **Calls:** parametrize, add_url_rule, get, loads, jsonify


### `test_jsonify_dicts(self, app, client) → None`


Test jsonify with dicts and kwargs unpacking.


- **Line:** 161–186
- **Complexity:** 4
- **Calls:** route, jsonify, get, loads


### `return_kwargs() → None`



- **Line:** 176–177
- **Complexity:** 1
- **Calls:** route, jsonify


### `return_dict() → None`



- **Line:** 180–181
- **Complexity:** 1
- **Calls:** route, jsonify


### `test_jsonify_arrays(self, app, client) → None`


Test jsonify of lists and args unpacking.


- **Line:** 188–213
- **Complexity:** 4
- **Calls:** route, jsonify, get, loads


### `return_args_unpack() → None`



- **Line:** 203–204
- **Complexity:** 1
- **Calls:** route, jsonify


### `return_array() → None`



- **Line:** 207–208
- **Complexity:** 1
- **Calls:** route, jsonify


### `test_jsonify_date_types(self, app, client) → None`


Test jsonify with datetime.date and datetime.datetime types.


- **Line:** 215–227
- **Complexity:** 4
- **Calls:** enumerate, datetime, date, format, add_url_rule, get, str, http_date, jsonify, loads, timetuple


### `test_jsonify_aware_datetimes(self, tz) → None`


Test if aware datetime.datetime objects are converted into GMT.


- **Line:** 230–236
- **Complexity:** 2
- **Calls:** parametrize, FixedOffset, datetime, strftime, encode, astimezone, JSONEncoder


### `test_jsonify_uuid_types(self, app, client) → None`


Test jsonify with uuid.UUID types


- **Line:** 238–250
- **Complexity:** 3
- **Calls:** UUID, add_url_rule, get, loads, str, jsonify


### `test_json_attr(self, app, client) → None`



- **Line:** 252–263
- **Complexity:** 2
- **Calls:** route, post, get_json, text_type, dumps


### `add() → None`



- **Line:** 254–256
- **Complexity:** 1
- **Calls:** route, get_json, text_type


### `test_template_escaping(self, app, req_ctx) → None`



- **Line:** 265–283
- **Complexity:** 9
- **Calls:** htmlsafe_dumps, render, type


### `test_json_customization(self, app, client) → None`



- **Line:** 285–318
- **Complexity:** 2
- **Calls:** route, post, dumps, isinstance, default, setdefault, __init__, X, get_json, len


### `__init__(self, val) → None`



- **Line:** 287–288
- **Complexity:** 1
- **Calls:** none


### `default(self, o) → None`



- **Line:** 291–294
- **Complexity:** 1
- **Calls:** isinstance, default


### `__init__(self) → None`



- **Line:** 297–299
- **Complexity:** 1
- **Calls:** setdefault, __init__


### `object_hook(self, obj) → None`



- **Line:** 301–304
- **Complexity:** 1
- **Calls:** X, len


### `index() → None`



- **Line:** 310–311
- **Complexity:** 1
- **Calls:** route, dumps, get_json


### `test_blueprint_json_customization(self, app, client) → None`



- **Line:** 320–358
- **Complexity:** 2
- **Calls:** Blueprint, route, register_blueprint, post, dumps, isinstance, default, setdefault, __init__, X, get_json, len


### `__init__(self, val) → None`



- **Line:** 322–323
- **Complexity:** 1
- **Calls:** none


### `default(self, o) → None`



- **Line:** 326–330
- **Complexity:** 1
- **Calls:** isinstance, default


### `__init__(self) → None`



- **Line:** 333–335
- **Complexity:** 1
- **Calls:** setdefault, __init__


### `object_hook(self, obj) → None`



- **Line:** 337–341
- **Complexity:** 1
- **Calls:** X, len


### `index() → None`



- **Line:** 348–349
- **Complexity:** 1
- **Calls:** route, dumps, get_json


### `test_modified_url_encoding(self, app, client) → None`



- **Line:** 363–376
- **Complexity:** 3
- **Calls:** skipif, route, get, encode, has_encoding


### `index() → None`



- **Line:** 371–372
- **Complexity:** 1
- **Calls:** route


### `test_json_key_sorting(self, app, client) → None`



- **Line:** 378–446
- **Complexity:** 6
- **Calls:** fromkeys, route, get, range, jsonify, strip, splitlines, decode


### `index() → None`



- **Line:** 385–386
- **Complexity:** 1
- **Calls:** route, jsonify


### `test_send_file_regular(self, app, req_ctx) → None`



- **Line:** 450–457
- **Complexity:** 4
- **Calls:** send_file, close, open_resource, read


### `test_send_file_xsendfile(self, app, req_ctx) → None`



- **Line:** 459–468
- **Complexity:** 5
- **Calls:** send_file, close, join


### `test_send_file_last_modified(self, app, client) → None`



- **Line:** 470–482
- **Complexity:** 2
- **Calls:** datetime, route, get, send_file, StringIO


### `index() → None`



- **Line:** 474–479
- **Complexity:** 1
- **Calls:** route, send_file, StringIO


### `test_send_file_object_without_mimetype(self, app, req_ctx) → None`



- **Line:** 484–490
- **Complexity:** 3
- **Calls:** send_file, raises, str, StringIO


### `test_send_file_object(self, app, req_ctx) → None`



- **Line:** 492–544
- **Complexity:** 12
- **Calls:** StringIO, send_file, close, PyStringIO, open, join, open_resource, getattr, read


### `__init__(self) → None`



- **Line:** 518–519
- **Complexity:** 1
- **Calls:** StringIO


### `__getattr__(self, name) → None`



- **Line:** 521–522
- **Complexity:** 1
- **Calls:** getattr


### `test_send_file_pathlike(self, app, req_ctx) → None`



- **Line:** 546–553
- **Complexity:** 4
- **Calls:** send_file, close, FakePath, open_resource, read


### `test_send_file_range_request(self, app, client) → None`



- **Line:** 559–618
- **Complexity:** 14
- **Calls:** skipif, route, get, close, replace, send_file, open_resource, callable, utcfromtimestamp, getattr, read, getmtime, http_date, join, datetime


### `index() → None`



- **Line:** 561–562
- **Complexity:** 1
- **Calls:** route, send_file


### `test_send_file_range_request_bytesio(self, app, client) → None`



- **Line:** 620–631
- **Complexity:** 3
- **Calls:** route, get, close, BytesIO, send_file


### `index() → None`



- **Line:** 622–626
- **Complexity:** 1
- **Calls:** route, BytesIO, send_file


### `test_send_file_range_request_xsendfile_invalid(self, app, client) → None`



- **Line:** 637–647
- **Complexity:** 2
- **Calls:** skipif, route, get, close, send_file, callable, getattr


### `index() → None`



- **Line:** 642–643
- **Complexity:** 1
- **Calls:** route, send_file


### `test_attachment(self, app, req_ctx) → None`



- **Line:** 649–686
- **Complexity:** 10
- **Calls:** Flask, send_file, parse_options_header, close, test_request_context, open, StringIO, join


### `test_attachment_filename_encoding(self, filename, ascii, utf8) → None`



- **Line:** 705–715
- **Complexity:** 5
- **Calls:** usefixtures, parametrize, send_file, close


### `test_static_file(self, app, req_ctx) → None`



- **Line:** 717–764
- **Complexity:** 8
- **Calls:** send_static_file, parse_cache_control_header, close, send_file, StaticFileApp, FakePath, test_request_context


### `get_send_file_max_age(self, filename) → None`



- **Line:** 750–751
- **Complexity:** 1
- **Calls:** none


### `test_send_from_directory(self, app, req_ctx) → None`



- **Line:** 766–773
- **Complexity:** 2
- **Calls:** join, send_from_directory, close, dirname, strip


### `test_send_from_directory_pathlike(self, app, req_ctx) → None`



- **Line:** 775–782
- **Complexity:** 2
- **Calls:** join, send_from_directory, close, dirname, FakePath, strip


### `test_send_from_directory_null_character(self, app, req_ctx) → None`



- **Line:** 784–795
- **Complexity:** 2
- **Calls:** join, dirname, raises, send_from_directory


### `test_url_for_with_anchor(self, app, req_ctx) → None`



- **Line:** 799–804
- **Complexity:** 2
- **Calls:** route, url_for


### `index() → None`



- **Line:** 801–802
- **Complexity:** 1
- **Calls:** route


### `test_url_for_with_scheme(self, app, req_ctx) → None`



- **Line:** 806–814
- **Complexity:** 2
- **Calls:** route, url_for


### `index() → None`



- **Line:** 808–809
- **Complexity:** 1
- **Calls:** route


### `test_url_for_with_scheme_not_external(self, app, req_ctx) → None`



- **Line:** 816–821
- **Complexity:** 1
- **Calls:** route, raises


### `index() → None`



- **Line:** 818–819
- **Complexity:** 1
- **Calls:** route


### `test_url_for_with_alternating_schemes(self, app, req_ctx) → None`



- **Line:** 823–833
- **Complexity:** 4
- **Calls:** route, url_for


### `index() → None`



- **Line:** 825–826
- **Complexity:** 1
- **Calls:** route


### `test_url_with_method(self, app, req_ctx) → None`



- **Line:** 835–854
- **Complexity:** 4
- **Calls:** as_view, add_url_rule, url_for


### `get(self, id) → None`



- **Line:** 839–842
- **Complexity:** 1
- **Calls:** none


### `post(self) → None`



- **Line:** 844–845
- **Complexity:** 1
- **Calls:** none


### `test_name_with_import_error(self, modules_tmpdir) → None`



- **Line:** 868–873
- **Complexity:** 2
- **Calls:** write, Flask, join, AssertionError


### `test_streaming_with_context(self, app, client) → None`



- **Line:** 877–888
- **Complexity:** 2
- **Calls:** route, get, Response, stream_with_context, generate


### `index() → None`



- **Line:** 879–885
- **Complexity:** 1
- **Calls:** route, Response, stream_with_context, generate


### `generate() → None`



- **Line:** 880–883
- **Complexity:** 1
- **Calls:** none


### `test_streaming_with_context_as_decorator(self, app, client) → None`



- **Line:** 890–902
- **Complexity:** 2
- **Calls:** route, get, Response, generate


### `index() → None`



- **Line:** 892–899
- **Complexity:** 1
- **Calls:** route, Response, generate


### `generate(hello) → None`



- **Line:** 894–897
- **Complexity:** 1
- **Calls:** none


### `test_streaming_with_context_and_custom_close(self, app, client) → None`



- **Line:** 904–933
- **Complexity:** 3
- **Calls:** route, get, Response, append, next, stream_with_context, Wrapper, generate


### `__init__(self, gen) → None`



- **Line:** 908–909
- **Complexity:** 1
- **Calls:** none


### `__iter__(self) → None`



- **Line:** 911–912
- **Complexity:** 1
- **Calls:** none


### `close(self) → None`



- **Line:** 914–915
- **Complexity:** 1
- **Calls:** append


### `__next__(self) → None`



- **Line:** 917–918
- **Complexity:** 1
- **Calls:** next


### `index() → None`



- **Line:** 923–929
- **Complexity:** 1
- **Calls:** route, Response, stream_with_context, Wrapper, generate


### `generate() → None`



- **Line:** 924–927
- **Complexity:** 1
- **Calls:** none


### `test_stream_keeps_session(self, app, client) → None`



- **Line:** 935–947
- **Complexity:** 2
- **Calls:** route, get, Response, gen


### `index() → None`



- **Line:** 937–944
- **Complexity:** 1
- **Calls:** route, Response, gen


### `gen() → None`



- **Line:** 941–942
- **Complexity:** 1
- **Calls:** none


### `test_safe_join(self) → None`



- **Line:** 951–971
- **Complexity:** 3
- **Calls:** safe_join


### `test_safe_join_exceptions(self) → None`



- **Line:** 973–988
- **Complexity:** 2
- **Calls:** raises, print, safe_join


### `test_get_debug_flag(self, monkeypatch, debug, expected_flag, expected_default_flag) → None`



- **Line:** 1002–1010
- **Complexity:** 5
- **Calls:** parametrize, setenv, get_debug_flag


### `test_get_env(self, monkeypatch, env, ref_env, debug) → None`



- **Line:** 1021–1024
- **Complexity:** 3
- **Calls:** parametrize, setenv, get_debug_flag, get_env


### `test_make_response(self) → None`



- **Line:** 1026–1036
- **Complexity:** 6
- **Calls:** Flask, test_request_context, make_response


### `test_open_resource(self, mode) → None`



- **Line:** 1039–1043
- **Complexity:** 2
- **Calls:** parametrize, Flask, open_resource, str, read


### `test_open_resource_exceptions(self, mode) → None`



- **Line:** 1046–1050
- **Complexity:** 1
- **Calls:** parametrize, Flask, raises, open_resource



## Classes


### `FakePath`


Fake object to represent a ``PathLike object``.

This represents a ``pathlib.Path`` object in python 3.
See: https://www.python.org/dev/peps/pep-0519/


- **Bases:** object
- **Methods:** __init__, __fspath__


### `FixedOffset`


Fixed offset in hours east from UTC.

This is a slight adaptation of the ``FixedOffset`` example found in
https://docs.python.org/2.7/library/datetime.html.


- **Bases:** datetime.tzinfo
- **Methods:** __init__, utcoffset, tzname, dst


### `TestJSON`



- **Bases:** object
- **Methods:** test_detect_encoding, test_bad_request_debug_message, test_json_bad_requests, test_json_custom_mimetypes, test_json_as_unicode, test_json_dump_to_file, test_jsonify_basic_types, test_jsonify_dicts, test_jsonify_arrays, test_jsonify_date_types, test_jsonify_aware_datetimes, test_jsonify_uuid_types, test_json_attr, test_template_escaping, test_json_customization, test_blueprint_json_customization, test_modified_url_encoding, test_json_key_sorting


### `X`



- **Bases:** object
- **Methods:** __init__


### `MyEncoder`



- **Bases:** flask.json.JSONEncoder
- **Methods:** default


### `MyDecoder`



- **Bases:** flask.json.JSONDecoder
- **Methods:** __init__, object_hook


### `X`



- **Bases:** object
- **Methods:** __init__


### `MyEncoder`



- **Bases:** flask.json.JSONEncoder
- **Methods:** default


### `MyDecoder`



- **Bases:** flask.json.JSONDecoder
- **Methods:** __init__, object_hook


### `ModifiedRequest`



- **Bases:** flask.Request
- **Methods:** none


### `TestSendfile`



- **Bases:** object
- **Methods:** test_send_file_regular, test_send_file_xsendfile, test_send_file_last_modified, test_send_file_object_without_mimetype, test_send_file_object, test_send_file_pathlike, test_send_file_range_request, test_send_file_range_request_bytesio, test_send_file_range_request_xsendfile_invalid, test_attachment, test_attachment_filename_encoding, test_static_file, test_send_from_directory, test_send_from_directory_pathlike, test_send_from_directory_null_character


### `PyStringIO`



- **Bases:** object
- **Methods:** __init__, __getattr__


### `StaticFileApp`



- **Bases:** flask.Flask
- **Methods:** get_send_file_max_age


### `TestUrlFor`



- **Bases:** object
- **Methods:** test_url_for_with_anchor, test_url_for_with_scheme, test_url_for_with_scheme_not_external, test_url_for_with_alternating_schemes, test_url_with_method


### `MyView`



- **Bases:** MethodView
- **Methods:** get, post


### `TestNoImports`


Test Flasks are created without import.

Avoiding ``__import__`` helps create Flask instances where there are errors
at import time.  Those runtime errors will be apparent to the user soon
enough, but tools which build Flask instances meta-programmatically benefit
from a Flask which does not ``__import__``.  Instead of importing to
retrieve file paths or metadata on a module or package, use the pkgutil and
imp modules in the Python standard library.


- **Bases:** object
- **Methods:** test_name_with_import_error


### `TestStreaming`



- **Bases:** object
- **Methods:** test_streaming_with_context, test_streaming_with_context_as_decorator, test_streaming_with_context_and_custom_close, test_stream_keeps_session


### `Wrapper`



- **Bases:** object
- **Methods:** __init__, __iter__, close, __next__


### `TestSafeJoin`



- **Bases:** object
- **Methods:** test_safe_join, test_safe_join_exceptions


### `TestHelpers`



- **Bases:** object
- **Methods:** test_get_debug_flag, test_get_env, test_make_response, test_open_resource, test_open_resource_exceptions

