# Code-Archon Investigation Report

**Goal:** Understand the routing system
**Session:** sess_a24fc260
**Generated:** 2026-10-09T15:29:29.425504+00:00

---

## Summary

| Metric | Value |
|--------|-------|
| Modules documented | 73 |
| Verified findings | 0 |
| Average confidence | 0.00 |
| Unknowns remaining | 5 |

---

## Verified Findings



---

## Modules


### `docs/conf.py`

- **Lines:** 96
- **Avg Complexity:** 3.0
- **Imports:** packaging.version, pallets_sphinx_themes.get_version, pallets_sphinx_themes.ProjectLink, docutils.nodes.reference, docutils.parsers.rst.roles.set_classes


### `examples/javascript/js_example/__init__.py`

- **Lines:** 5
- **Avg Complexity:** 0.0
- **Imports:** flask.Flask, js_example.views


### `examples/javascript/js_example/views.py`

- **Lines:** 18
- **Avg Complexity:** 1.0
- **Imports:** flask.jsonify, flask.render_template, flask.request, js_example.app


### `examples/javascript/setup.py`

- **Lines:** 23
- **Avg Complexity:** 0.0
- **Imports:** io, setuptools.find_packages, setuptools.setup


### `examples/javascript/tests/conftest.py`

- **Lines:** 15
- **Avg Complexity:** 1.0
- **Imports:** pytest, js_example.app


### `examples/javascript/tests/test_js_example.py`

- **Lines:** 27
- **Avg Complexity:** 1.5
- **Imports:** pytest, flask.template_rendered


### `examples/tutorial/flaskr/__init__.py`

- **Lines:** 50
- **Avg Complexity:** 3.0
- **Imports:** os, flask.Flask, flaskr.db, flaskr.auth, flaskr.blog


### `examples/tutorial/flaskr/auth.py`

- **Lines:** 116
- **Avg Complexity:** 3.0
- **Imports:** functools, flask.Blueprint, flask.flash, flask.g, flask.redirect, flask.render_template, flask.request, flask.session, flask.url_for, werkzeug.security.check_password_hash, werkzeug.security.generate_password_hash, flaskr.db.get_db


### `examples/tutorial/flaskr/blog.py`

- **Lines:** 125
- **Avg Complexity:** 2.8
- **Imports:** flask.Blueprint, flask.flash, flask.g, flask.redirect, flask.render_template, flask.request, flask.url_for, werkzeug.exceptions.abort, flaskr.auth.login_required, flaskr.db.get_db


### `examples/tutorial/flaskr/db.py`

- **Lines:** 54
- **Avg Complexity:** 1.4
- **Imports:** sqlite3, click, flask.current_app, flask.g, flask.cli.with_appcontext


### `examples/tutorial/setup.py`

- **Lines:** 23
- **Avg Complexity:** 0.0
- **Imports:** io, setuptools.find_packages, setuptools.setup


### `examples/tutorial/tests/conftest.py`

- **Lines:** 62
- **Avg Complexity:** 1.1
- **Imports:** os, tempfile, pytest, flaskr.create_app, flaskr.db.get_db, flaskr.db.init_db


### `examples/tutorial/tests/test_auth.py`

- **Lines:** 69
- **Avg Complexity:** 3.0
- **Imports:** pytest, flask.g, flask.session, flaskr.db.get_db


### `examples/tutorial/tests/test_blog.py`

- **Lines:** 83
- **Avg Complexity:** 3.2
- **Imports:** pytest, flaskr.db.get_db


### `examples/tutorial/tests/test_db.py`

- **Lines:** 29
- **Avg Complexity:** 3.0
- **Imports:** sqlite3, pytest, flaskr.db.get_db


### `examples/tutorial/tests/test_factory.py`

- **Lines:** 12
- **Avg Complexity:** 2.5
- **Imports:** flaskr.create_app


### `setup.py`

- **Lines:** 80
- **Avg Complexity:** 0.0
- **Imports:** io, re, setuptools.find_packages, setuptools.setup


### `src/flask/__init__.py`

- **Lines:** 60
- **Avg Complexity:** 0.0
- **Imports:** jinja2.escape, jinja2.Markup, werkzeug.exceptions.abort, werkzeug.utils.redirect, json, _compat.json_available, app.Flask, app.Request, app.Response, blueprints.Blueprint, config.Config, ctx.after_this_request, ctx.copy_current_request_context, ctx.has_app_context, ctx.has_request_context, globals._app_ctx_stack, globals._request_ctx_stack, globals.current_app, globals.g, globals.request, globals.session, helpers.flash, helpers.get_flashed_messages, helpers.get_template_attribute, helpers.make_response, helpers.safe_join, helpers.send_file, helpers.send_from_directory, helpers.stream_with_context, helpers.url_for, json.jsonify, signals.appcontext_popped, signals.appcontext_pushed, signals.appcontext_tearing_down, signals.before_render_template, signals.got_request_exception, signals.message_flashed, signals.request_finished, signals.request_started, signals.request_tearing_down, signals.signals_available, signals.template_rendered, templating.render_template, templating.render_template_string


### `src/flask/__main__.py`

- **Lines:** 15
- **Avg Complexity:** 0.0
- **Imports:** cli.main


### `src/flask/_compat.py`

- **Lines:** 145
- **Avg Complexity:** 1.5
- **Imports:** sys, inspect.getfullargspec, io.StringIO, collections.abc, inspect.getargspec, cStringIO.StringIO, collections, os.fspath, warnings


### `src/flask/app.py`

- **Lines:** 2467
- **Avg Complexity:** 2.8
- **Imports:** os, sys, warnings, datetime.timedelta, functools.update_wrapper, itertools.chain, threading.Lock, werkzeug.datastructures.Headers, werkzeug.datastructures.ImmutableDict, werkzeug.exceptions.BadRequest, werkzeug.exceptions.BadRequestKeyError, werkzeug.exceptions.default_exceptions, werkzeug.exceptions.HTTPException, werkzeug.exceptions.InternalServerError, werkzeug.exceptions.MethodNotAllowed, werkzeug.routing.BuildError, werkzeug.routing.Map, werkzeug.routing.RequestRedirect, werkzeug.routing.RoutingException, werkzeug.routing.Rule, werkzeug.wrappers.BaseResponse, cli, json, _compat.integer_types, _compat.reraise, _compat.string_types, _compat.text_type, config.Config, config.ConfigAttribute, ctx._AppCtxGlobals, ctx.AppContext, ctx.RequestContext, globals._request_ctx_stack, globals.g, globals.request, globals.session, helpers._endpoint_from_view_func, helpers._PackageBoundObject, helpers.find_package, helpers.get_debug_flag, helpers.get_env, helpers.get_flashed_messages, helpers.get_load_dotenv, helpers.locked_cached_property, helpers.url_for, json.jsonify, logging.create_logger, sessions.SecureCookieSessionInterface, signals.appcontext_tearing_down, signals.got_request_exception, signals.request_finished, signals.request_started, signals.request_tearing_down, templating._default_template_ctx_processor, templating.DispatchingJinjaLoader, templating.Environment, wrappers.Request, wrappers.Response, werkzeug.serving.run_simple, debughelpers.FormDataRoutingRedirect, testing.EnvironBuilder, debughelpers.explain_ignored_app_run, testing.FlaskClient, testing.FlaskCliRunner


### `src/flask/blueprints.py`

- **Lines:** 569
- **Avg Complexity:** 1.6
- **Imports:** functools.update_wrapper, helpers._endpoint_from_view_func, helpers._PackageBoundObject, warnings.warn


### `src/flask/cli.py`

- **Lines:** 971
- **Avg Complexity:** 4.3
- **Imports:** __future__.print_function, ast, inspect, os, platform, re, sys, traceback, functools.update_wrapper, operator.attrgetter, threading.Lock, threading.Thread, click, werkzeug.utils.import_string, _compat.getargspec, _compat.itervalues, _compat.reraise, _compat.text_type, globals.current_app, helpers.get_debug_flag, helpers.get_env, helpers.get_load_dotenv, dotenv, ssl, Flask, Flask, werkzeug, __version__, werkzeug.serving.run_simple, code, globals._app_ctx_stack, pkg_resources, OpenSSL


### `src/flask/config.py`

- **Lines:** 269
- **Avg Complexity:** 3.4
- **Imports:** errno, os, types, werkzeug.utils.import_string, json, _compat.iteritems, _compat.string_types


### `src/flask/ctx.py`

- **Lines:** 475
- **Avg Complexity:** 2.4
- **Imports:** sys, functools.update_wrapper, werkzeug.exceptions.HTTPException, _compat.BROKEN_PYPY_CTXMGR_EXIT, _compat.reraise, globals._app_ctx_stack, globals._request_ctx_stack, signals.appcontext_popped, signals.appcontext_pushed


### `src/flask/debughelpers.py`

- **Lines:** 183
- **Avg Complexity:** 3.8
- **Imports:** os, warnings.warn, _compat.implements_to_string, _compat.text_type, app.Flask, blueprints.Blueprint, globals._request_ctx_stack


### `src/flask/globals.py`

- **Lines:** 62
- **Avg Complexity:** 2.0
- **Imports:** functools.partial, werkzeug.local.LocalProxy, werkzeug.local.LocalStack


### `src/flask/helpers.py`

- **Lines:** 1155
- **Avg Complexity:** 4.5
- **Imports:** io, mimetypes, os, pkgutil, posixpath, socket, sys, unicodedata, functools.update_wrapper, threading.RLock, time.time, zlib.adler32, jinja2.FileSystemLoader, werkzeug.datastructures.Headers, werkzeug.exceptions.BadRequest, werkzeug.exceptions.NotFound, werkzeug.exceptions.RequestedRangeNotSatisfiable, werkzeug.routing.BuildError, werkzeug.urls.url_quote, werkzeug.wsgi.wrap_file, _compat.fspath, _compat.PY2, _compat.string_types, _compat.text_type, globals._app_ctx_stack, globals._request_ctx_stack, globals.current_app, globals.request, globals.session, signals.message_flashed, warnings.warn, importlib.util, cli.AppGroup


### `src/flask/json/__init__.py`

- **Lines:** 376
- **Avg Complexity:** 4.2
- **Imports:** codecs, io, uuid, datetime.date, datetime.datetime, itsdangerous.json, jinja2.Markup, werkzeug.http.http_date, _compat.PY2, _compat.text_type, globals.current_app, globals.request, dataclasses


### `src/flask/json/tag.py`

- **Lines:** 309
- **Avg Complexity:** 2.2
- **Imports:** base64.b64decode, base64.b64encode, datetime.datetime, uuid.UUID, jinja2.Markup, werkzeug.http.http_date, werkzeug.http.parse_date, _compat.iteritems, _compat.text_type, json.dumps, json.loads


### `src/flask/logging.py`

- **Lines:** 109
- **Avg Complexity:** 4.5
- **Imports:** __future__.absolute_import, logging, sys, warnings, werkzeug.local.LocalProxy, globals.request


### `src/flask/sessions.py`

- **Lines:** 388
- **Avg Complexity:** 2.2
- **Imports:** hashlib, warnings, datetime.datetime, itsdangerous.BadSignature, itsdangerous.URLSafeTimedSerializer, werkzeug.datastructures.CallbackDict, _compat.collections_abc, helpers.is_ip, helpers.total_seconds, json.tag.TaggedJSONSerializer


### `src/flask/signals.py`

- **Lines:** 65
- **Avg Complexity:** 1.3
- **Imports:** blinker.Namespace


### `src/flask/templating.py`

- **Lines:** 155
- **Avg Complexity:** 2.8
- **Imports:** jinja2.BaseLoader, jinja2.Environment, jinja2.TemplateNotFound, globals._app_ctx_stack, globals._request_ctx_stack, signals.before_render_template, signals.template_rendered, debughelpers.explain_template_loading_attempts


### `src/flask/testing.py`

- **Lines:** 283
- **Avg Complexity:** 3.2
- **Imports:** warnings, contextlib.contextmanager, werkzeug.test, click.testing.CliRunner, werkzeug.test.Client, werkzeug.urls.url_parse, _request_ctx_stack, cli.ScriptInfo, json.dumps


### `src/flask/views.py`

- **Lines:** 163
- **Avg Complexity:** 5.0
- **Imports:** _compat.with_metaclass, globals.request


### `src/flask/wrappers.py`

- **Lines:** 137
- **Avg Complexity:** 2.9
- **Imports:** werkzeug.exceptions.BadRequest, werkzeug.wrappers.Request, werkzeug.wrappers.Response, werkzeug.wrappers.json.JSONMixin, json, globals.current_app, debughelpers.attach_enctype_error_multidict


### `tests/conftest.py`

- **Lines:** 202
- **Avg Complexity:** 1.3
- **Imports:** os, pkgutil, sys, textwrap, pytest, _pytest.monkeypatch, flask, flask.Flask, subprocess


### `tests/test_appctx.py`

- **Lines:** 220
- **Avg Complexity:** 3.1
- **Imports:** pytest, flask


### `tests/test_apps/blueprintapp/__init__.py`

- **Lines:** 9
- **Avg Complexity:** 0.0
- **Imports:** flask.Flask, blueprintapp.apps.admin.admin, blueprintapp.apps.frontend.frontend


### `tests/test_apps/blueprintapp/apps/__init__.py`

- **Lines:** 0
- **Avg Complexity:** 0.0
- **Imports:** none


### `tests/test_apps/blueprintapp/apps/admin/__init__.py`

- **Lines:** 20
- **Avg Complexity:** 1.0
- **Imports:** flask.Blueprint, flask.render_template


### `tests/test_apps/blueprintapp/apps/frontend/__init__.py`

- **Lines:** 14
- **Avg Complexity:** 1.0
- **Imports:** flask.Blueprint, flask.render_template


### `tests/test_apps/cliapp/__init__.py`

- **Lines:** 0
- **Avg Complexity:** 0.0
- **Imports:** none


### `tests/test_apps/cliapp/app.py`

- **Lines:** 6
- **Avg Complexity:** 0.0
- **Imports:** __future__.absolute_import, __future__.print_function, flask.Flask


### `tests/test_apps/cliapp/factory.py`

- **Lines:** 20
- **Avg Complexity:** 1.0
- **Imports:** __future__.absolute_import, __future__.print_function, flask.Flask


### `tests/test_apps/cliapp/importerrorapp.py`

- **Lines:** 8
- **Avg Complexity:** 0.0
- **Imports:** __future__.absolute_import, __future__.print_function, flask.Flask


### `tests/test_apps/cliapp/inner1/__init__.py`

- **Lines:** 3
- **Avg Complexity:** 0.0
- **Imports:** flask.Flask


### `tests/test_apps/cliapp/inner1/inner2/__init__.py`

- **Lines:** 0
- **Avg Complexity:** 0.0
- **Imports:** none


### `tests/test_apps/cliapp/inner1/inner2/flask.py`

- **Lines:** 3
- **Avg Complexity:** 0.0
- **Imports:** flask.Flask


### `tests/test_apps/cliapp/multiapp.py`

- **Lines:** 7
- **Avg Complexity:** 0.0
- **Imports:** __future__.absolute_import, __future__.print_function, flask.Flask


### `tests/test_apps/helloworld/hello.py`

- **Lines:** 8
- **Avg Complexity:** 1.0
- **Imports:** flask.Flask


### `tests/test_apps/helloworld/wsgi.py`

- **Lines:** 1
- **Avg Complexity:** 0.0
- **Imports:** hello.app


### `tests/test_apps/subdomaintestmodule/__init__.py`

- **Lines:** 4
- **Avg Complexity:** 0.0
- **Imports:** flask.Module


### `tests/test_basic.py`

- **Lines:** 1987
- **Avg Complexity:** 3.9
- **Imports:** re, sys, time, uuid, datetime.datetime, threading.Thread, pytest, werkzeug.serving, werkzeug.exceptions.BadRequest, werkzeug.exceptions.Forbidden, werkzeug.exceptions.NotFound, werkzeug.http.parse_date, werkzeug.routing.BuildError, flask, flask._compat.text_type, werkzeug.routing.Submount, werkzeug.routing.Rule, werkzeug.routing.Submount, werkzeug.routing.Rule, flask.debughelpers.DebugFilesKeyError, dataclasses.make_dataclass, pathlib.Path


### `tests/test_blueprints.py`

- **Lines:** 863
- **Avg Complexity:** 3.6
- **Imports:** functools, pytest, jinja2.TemplateNotFound, werkzeug.http.parse_cache_control_header, flask, flask._compat.text_type, blueprintapp.app, blueprintapp.app, werkzeug.routing.Rule


### `tests/test_cli.py`

- **Lines:** 667
- **Avg Complexity:** 3.4
- **Imports:** __future__.absolute_import, os, ssl, sys, types, functools.partial, click, pytest, _pytest.monkeypatch.notset, click.testing.CliRunner, flask.Blueprint, flask.current_app, flask.Flask, flask.cli.AppGroup, flask.cli.dotenv, flask.cli.find_best_app, flask.cli.FlaskGroup, flask.cli.get_version, flask.cli.load_dotenv, flask.cli.locate_app, flask.cli.NoAppException, flask.cli.prepare_import, flask.cli.run_command, flask.cli.ScriptInfo, flask.cli.with_appcontext, cliapp.app.testapp, flask.__version__, werkzeug.__version__, platform.python_version


### `tests/test_config.py`

- **Lines:** 202
- **Avg Complexity:** 3.2
- **Imports:** os, textwrap, datetime.timedelta, pytest, flask, flask._compat.PY2


### `tests/test_converters.py`

- **Lines:** 40
- **Avg Complexity:** 2.5
- **Imports:** werkzeug.routing.BaseConverter, flask.has_request_context, flask.url_for


### `tests/test_deprecations.py`

- **Lines:** 12
- **Avg Complexity:** 5.0
- **Imports:** pytest, flask.json_available


### `tests/test_helpers.py`

- **Lines:** 1050
- **Avg Complexity:** 3.4
- **Imports:** datetime, io, os, sys, uuid, pytest, werkzeug.datastructures.Range, werkzeug.exceptions.BadRequest, werkzeug.exceptions.NotFound, werkzeug.http.http_date, werkzeug.http.parse_cache_control_header, werkzeug.http.parse_options_header, flask, flask.json, flask._compat.StringIO, flask._compat.text_type, flask.helpers.get_debug_flag, flask.helpers.get_env, codecs, flask.views.MethodView


### `tests/test_instance_config.py`

- **Lines:** 144
- **Avg Complexity:** 2.1
- **Imports:** os, sys, pytest, flask, flask._compat.PY2, main_app.app, config_module_app.app, config_package_app.app, site_app.app, installed_package.app, site_package, site_egg, unimportable


### `tests/test_json_tag.py`

- **Lines:** 93
- **Avg Complexity:** 2.2
- **Imports:** datetime.datetime, uuid.uuid4, pytest, flask.Markup, flask.json.tag.JSONTag, flask.json.tag.TaggedJSONSerializer


### `tests/test_logging.py`

- **Lines:** 115
- **Avg Complexity:** 3.5
- **Imports:** logging, sys, pytest, flask._compat.StringIO, flask.logging.default_handler, flask.logging.has_level_handler, flask.logging.wsgi_errors_stream


### `tests/test_meta.py`

- **Lines:** 6
- **Avg Complexity:** 1.0
- **Imports:** io


### `tests/test_regression.py`

- **Lines:** 97
- **Avg Complexity:** 2.3
- **Imports:** gc, sys, threading, pytest, werkzeug.exceptions.NotFound, flask, flask.helpers.safe_join


### `tests/test_reqctx.py`

- **Lines:** 285
- **Avg Complexity:** 3.2
- **Imports:** pytest, flask, flask.sessions.SessionInterface, greenlet.greenlet, flask.testing.EnvironBuilder, flask.testing.EnvironBuilder


### `tests/test_signals.py`

- **Lines:** 206
- **Avg Complexity:** 4.0
- **Imports:** pytest, flask, blinker


### `tests/test_subclassing.py`

- **Lines:** 31
- **Avg Complexity:** 4.0
- **Imports:** flask, flask._compat.StringIO


### `tests/test_templating.py`

- **Lines:** 453
- **Avg Complexity:** 3.1
- **Imports:** logging, pytest, werkzeug.serving, jinja2.TemplateNotFound, flask, blueprintapp.app, jinja2.DictLoader


### `tests/test_testing.py`

- **Lines:** 447
- **Avg Complexity:** 3.9
- **Imports:** click, pytest, werkzeug, flask, flask.appcontext_popped, flask._compat.text_type, flask.cli.ScriptInfo, flask.json.jsonify, flask.testing.EnvironBuilder, flask.testing.FlaskCliRunner, flask.testing.make_test_environ_builder, blinker


### `tests/test_user_error_handler.py`

- **Lines:** 289
- **Avg Complexity:** 3.8
- **Imports:** pytest, werkzeug.exceptions.Forbidden, werkzeug.exceptions.HTTPException, werkzeug.exceptions.InternalServerError, werkzeug.exceptions.NotFound, flask


### `tests/test_views.py`

- **Lines:** 252
- **Avg Complexity:** 3.0
- **Imports:** pytest, werkzeug.http.parse_set_header, flask.views



---

## Unknowns



- Locate and analyze the `add_url_rule` method in the Flask class to see how URL rules are stored in the internal URL map.

- Examine the Blueprint class for its `route` decorator and how it registers rules with the parent Flask app.

- Trace the request handling flow in Flask (e.g., `full_dispatch_request` or `dispatch_request`) to see how the URL map is matched and the corresponding view function is invoked.

- Identify the data structures (e.g., `Map`, `Rule`) used for routing and how they are populated during app/blueprint initialization.

- Verify the routing behavior with a simple example by locating a test or example that defines a route and confirms the correct view function is called.

