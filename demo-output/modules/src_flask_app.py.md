# Module: `src/flask/app.py`

**Path:** `C:\temp\flask\src\flask\app.py`
**Lines:** 2467
**Avg Complexity:** 2.8


## Description

flask.app
~~~~~~~~~

This module implements the central WSGI application object.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `os`

- `sys`

- `warnings`

- `datetime.timedelta`

- `functools.update_wrapper`

- `itertools.chain`

- `threading.Lock`

- `werkzeug.datastructures.Headers`

- `werkzeug.datastructures.ImmutableDict`

- `werkzeug.exceptions.BadRequest`

- `werkzeug.exceptions.BadRequestKeyError`

- `werkzeug.exceptions.default_exceptions`

- `werkzeug.exceptions.HTTPException`

- `werkzeug.exceptions.InternalServerError`

- `werkzeug.exceptions.MethodNotAllowed`

- `werkzeug.routing.BuildError`

- `werkzeug.routing.Map`

- `werkzeug.routing.RequestRedirect`

- `werkzeug.routing.RoutingException`

- `werkzeug.routing.Rule`

- `werkzeug.wrappers.BaseResponse`

- `cli`

- `json`

- `_compat.integer_types`

- `_compat.reraise`

- `_compat.string_types`

- `_compat.text_type`

- `config.Config`

- `config.ConfigAttribute`

- `ctx._AppCtxGlobals`

- `ctx.AppContext`

- `ctx.RequestContext`

- `globals._request_ctx_stack`

- `globals.g`

- `globals.request`

- `globals.session`

- `helpers._endpoint_from_view_func`

- `helpers._PackageBoundObject`

- `helpers.find_package`

- `helpers.get_debug_flag`

- `helpers.get_env`

- `helpers.get_flashed_messages`

- `helpers.get_load_dotenv`

- `helpers.locked_cached_property`

- `helpers.url_for`

- `json.jsonify`

- `logging.create_logger`

- `sessions.SecureCookieSessionInterface`

- `signals.appcontext_tearing_down`

- `signals.got_request_exception`

- `signals.request_finished`

- `signals.request_started`

- `signals.request_tearing_down`

- `templating._default_template_ctx_processor`

- `templating.DispatchingJinjaLoader`

- `templating.Environment`

- `wrappers.Request`

- `wrappers.Response`

- `werkzeug.serving.run_simple`

- `debughelpers.FormDataRoutingRedirect`

- `testing.EnvironBuilder`

- `debughelpers.explain_ignored_app_run`

- `testing.FlaskClient`

- `testing.FlaskCliRunner`



## Functions


### `_make_timedelta(value) → None`



- **Line:** 76–79
- **Complexity:** 2
- **Calls:** isinstance, timedelta


### `setupmethod(f) → None`


Wraps a method so that it performs a check in debug mode if the
first request was already handled.


- **Line:** 82–100
- **Complexity:** 1
- **Calls:** update_wrapper, f, AssertionError


### `wrapper_func(self) → None`



- **Line:** 87–98
- **Complexity:** 1
- **Calls:** f, AssertionError


### `__init__(self, import_name, static_url_path, static_folder, static_host, host_matching, subdomain_matching, template_folder, instance_path, instance_relative_config, root_path) → None`



- **Line:** 402–610
- **Complexity:** 5
- **Calls:** __init__, make_config, url_map_class, Lock, auto_find_instance_path, add_url_rule, isabs, ValueError, bool


### `name(self) → None`


The name of the application.  This is usually the import name
with the difference that it's guessed from the run file if the
import name is main.  This name is used as a display name when
Flask needs the name of the application.  It can be set and overridden
to change the value.

.. versionadded:: 0.8


- **Line:** 613–627
- **Complexity:** 3
- **Calls:** getattr, splitext, basename


### `propagate_exceptions(self) → None`


Returns the value of the ``PROPAGATE_EXCEPTIONS`` configuration
value in case it's set, otherwise a sensible default is returned.

.. versionadded:: 0.7


- **Line:** 630–639
- **Complexity:** 3
- **Calls:** none


### `preserve_context_on_exception(self) → None`


Returns the value of the ``PRESERVE_CONTEXT_ON_EXCEPTION``
configuration value in case it's set, otherwise a sensible default
is returned.

.. versionadded:: 0.7


- **Line:** 642–652
- **Complexity:** 2
- **Calls:** none


### `logger(self) → None`


A standard Python :class:`~logging.Logger` for the app, with
the same name as :attr:`name`.

In debug mode, the logger's :attr:`~logging.Logger.level` will
be set to :data:`~logging.DEBUG`.

If there are no handlers configured, a default handler will be
added. See :doc:`/logging` for more information.

.. versionchanged:: 1.1.0
    The logger takes the same name as :attr:`name` rather than
    hard-coding ``"flask.app"``.

.. versionchanged:: 1.0.0
    Behavior was simplified. The logger is always named
    ``"flask.app"``. The level is only set during configuration,
    it doesn't check ``app.debug`` each time. Only one format is
    used, not different ones depending on ``app.debug``. No
    handlers are removed, and a handler is only added if no
    handlers are already configured.

.. versionadded:: 0.3


- **Line:** 655–679
- **Complexity:** 1
- **Calls:** create_logger


### `jinja_env(self) → None`


The Jinja environment used to load templates.

The environment is created the first time this property is
accessed. Changing :attr:`jinja_options` after that will have no
effect.


- **Line:** 682–689
- **Complexity:** 1
- **Calls:** create_jinja_environment


### `got_first_request(self) → None`


This attribute is set to ``True`` if the application started
handling the first request.

.. versionadded:: 0.8


- **Line:** 692–698
- **Complexity:** 1
- **Calls:** none


### `make_config(self, instance_relative) → None`


Used to create the config attribute by the Flask constructor.
The `instance_relative` parameter is passed in from the constructor
of Flask (there named `instance_relative_config`) and indicates if
the config should be relative to the instance path or the root path
of the application.

.. versionadded:: 0.8


- **Line:** 700–715
- **Complexity:** 2
- **Calls:** dict, get_env, get_debug_flag, config_class


### `auto_find_instance_path(self) → None`


Tries to locate the instance path if it was not provided to the
constructor of the application class.  It will basically calculate
the path to a folder named ``instance`` next to your main file or
the package.

.. versionadded:: 0.8


- **Line:** 717–728
- **Complexity:** 2
- **Calls:** find_package, join


### `open_instance_resource(self, resource, mode) → None`


Opens a resource from the application's instance folder
(:attr:`instance_path`).  Otherwise works like
:meth:`open_resource`.  Instance resources can also be opened for
writing.

:param resource: the name of the resource.  To access resources within
                 subfolders use forward slashes as separator.
:param mode: resource file opening mode, default is 'rb'.


- **Line:** 730–740
- **Complexity:** 1
- **Calls:** open, join


### `templates_auto_reload(self) → None`


Reload templates when they are changed. Used by
:meth:`create_jinja_environment`.

This attribute can be configured with :data:`TEMPLATES_AUTO_RELOAD`. If
not set, it will be enabled in debug mode.

.. versionadded:: 1.0
    This property was added but the underlying config and behavior
    already existed.


- **Line:** 743–755
- **Complexity:** 1
- **Calls:** none


### `templates_auto_reload(self, value) → None`



- **Line:** 758–759
- **Complexity:** 1
- **Calls:** none


### `create_jinja_environment(self) → None`


Create the Jinja environment based on :attr:`jinja_options`
and the various Jinja-related methods of the app. Changing
:attr:`jinja_options` after this will have no effect. Also adds
Flask-related globals and filters to the environment.

.. versionchanged:: 0.11
   ``Environment.auto_reload`` set in accordance with
   ``TEMPLATES_AUTO_RELOAD`` configuration option.

.. versionadded:: 0.5


- **Line:** 761–794
- **Complexity:** 3
- **Calls:** dict, jinja_environment, update


### `create_global_jinja_loader(self) → None`


Creates the loader for the Jinja2 environment.  Can be used to
override just the loader and keeping the rest unchanged.  It's
discouraged to override this function.  Instead one should override
the :meth:`jinja_loader` function instead.

The global loader dispatches between the loaders of the application
and the individual blueprints.

.. versionadded:: 0.7


- **Line:** 796–807
- **Complexity:** 1
- **Calls:** DispatchingJinjaLoader


### `select_jinja_autoescape(self, filename) → None`


Returns ``True`` if autoescaping should be active for the given
template name. If no template name is given, returns `True`.

.. versionadded:: 0.5


- **Line:** 809–817
- **Complexity:** 2
- **Calls:** endswith


### `update_template_context(self, context) → None`


Update the template context with some commonly used variables.
This injects request, session, config and g into the template
context as well as everything template context processors want
to inject.  Note that the as of Flask 0.6, the original values
in the context will not be overridden if a context processor
decides to return a value with the same key.

:param context: the context as a dictionary that is updated in place
                to add extra variables.


- **Line:** 819–842
- **Complexity:** 5
- **Calls:** copy, update, chain, func


### `make_shell_context(self) → None`


Returns the shell context for an interactive shell for this
application.  This runs all the registered shell context
processors.

.. versionadded:: 0.11


- **Line:** 844–854
- **Complexity:** 2
- **Calls:** update, processor


### `debug(self) → None`


Whether debug mode is enabled. When using ``flask run`` to start
the development server, an interactive debugger will be shown for
unhandled exceptions, and the server will be reloaded when code
changes. This maps to the :data:`DEBUG` config key. This is
enabled when :attr:`env` is ``'development'`` and is overridden
by the ``FLASK_DEBUG`` environment variable. It may not behave as
expected if set in code.

**Do not enable debug mode when deploying in production.**

Default: ``True`` if :attr:`env` is ``'development'``, or
``False`` otherwise.


- **Line:** 868–882
- **Complexity:** 1
- **Calls:** none


### `debug(self, value) → None`



- **Line:** 885–887
- **Complexity:** 1
- **Calls:** none


### `run(self, host, port, debug, load_dotenv) → None`


Runs the application on a local development server.

Do not use ``run()`` in a production setting. It is not intended to
meet security and performance requirements for a production server.
Instead, see :ref:`deployment` for WSGI server recommendations.

If the :attr:`debug` flag is set the server will automatically reload
for code changes and show a debugger in case an exception happened.

If you want to run the application in debug mode, but disable the
code execution on the interactive debugger, you can pass
``use_evalex=False`` as parameter.  This will keep the debugger's
traceback screen active, but disable code execution.

It is not recommended to use this function for development with
automatic reloading as this is badly supported.  Instead you should
be using the :command:`flask` command line script's ``run`` support.

.. admonition:: Keep in Mind

   Flask will suppress any server error with a generic error page
   unless it is in debug mode.  As such to enable just the
   interactive debugger without the code reloading, you have to
   invoke :meth:`run` with ``debug=True`` and ``use_reloader=False``.
   Setting ``use_debugger`` to ``True`` without being in debug mode
   won't catch any exceptions because there won't be any to
   catch.

:param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
    have the server available externally as well. Defaults to
    ``'127.0.0.1'`` or the host in the ``SERVER_NAME`` config variable
    if present.
:param port: the port of the webserver. Defaults to ``5000`` or the
    port defined in the ``SERVER_NAME`` config variable if present.
:param debug: if given, enable or disable debug mode. See
    :attr:`debug`.
:param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
    files to set environment variables. Will also change the working
    directory to the directory containing the first file found.
:param options: the options to be forwarded to the underlying Werkzeug
    server. See :func:`werkzeug.serving.run_simple` for more
    information.

.. versionchanged:: 1.0
    If installed, python-dotenv will be used to load environment
    variables from :file:`.env` and :file:`.flaskenv` files.

    If set, the :envvar:`FLASK_ENV` and :envvar:`FLASK_DEBUG`
    environment variables will override :attr:`env` and
    :attr:`debug`.

    Threaded mode is enabled by default.

.. versionchanged:: 0.10
    The default port is now picked from the ``SERVER_NAME``
    variable.


- **Line:** 889–995
- **Complexity:** 11
- **Calls:** get_load_dotenv, get, int, setdefault, show_server_banner, explain_ignored_app_run, load_dotenv, bool, partition, next, run_simple, get_env, get_debug_flag


### `test_client(self, use_cookies) → None`


Creates a test client for this application.  For information
about unit testing head over to :ref:`testing`.

Note that if you are testing for assertions or exceptions in your
application code, you must set ``app.testing = True`` in order for the
exceptions to propagate to the test client.  Otherwise, the exception
will be handled by the application (not visible to the test client) and
the only indication of an AssertionError or other exception will be a
500 status code response to the test client.  See the :attr:`testing`
attribute.  For example::

    app.testing = True
    client = app.test_client()

The test client can be used in a ``with`` block to defer the closing down
of the context until the end of the ``with`` block.  This is useful if
you want to access the context locals for testing::

    with app.test_client() as c:
        rv = c.get('/?vodka=42')
        assert request.args['vodka'] == '42'

Additionally, you may pass optional keyword arguments that will then
be passed to the application's :attr:`test_client_class` constructor.
For example::

    from flask.testing import FlaskClient

    class CustomClient(FlaskClient):
        def __init__(self, *args, **kwargs):
            self._authentication = kwargs.pop("authentication")
            super(CustomClient,self).__init__( *args, **kwargs)

    app.test_client_class = CustomClient
    client = app.test_client(authentication='Basic ....')

See :class:`~flask.testing.FlaskClient` for more information.

.. versionchanged:: 0.4
   added support for ``with`` block usage for the client.

.. versionadded:: 0.7
   The `use_cookies` parameter was added as well as the ability
   to override the client to be used by setting the
   :attr:`test_client_class` attribute.

.. versionchanged:: 0.11
   Added `**kwargs` to support passing additional keyword arguments to
   the constructor of :attr:`test_client_class`.


- **Line:** 997–1051
- **Complexity:** 2
- **Calls:** cls


### `test_cli_runner(self) → None`


Create a CLI runner for testing CLI commands.
See :ref:`testing-cli`.

Returns an instance of :attr:`test_cli_runner_class`, by default
:class:`~flask.testing.FlaskCliRunner`. The Flask app object is
passed as the first argument.

.. versionadded:: 1.0


- **Line:** 1053–1068
- **Complexity:** 2
- **Calls:** cls


### `open_session(self, request) → None`


Creates or opens a new session.  Default implementation stores all
session data in a signed cookie.  This requires that the
:attr:`secret_key` is set.  Instead of overriding this method
we recommend replacing the :class:`session_interface`.

.. deprecated: 1.0
    Will be removed in 2.0. Use
    ``session_interface.open_session`` instead.

:param request: an instance of :attr:`request_class`.


- **Line:** 1070–1089
- **Complexity:** 1
- **Calls:** warn, open_session, DeprecationWarning


### `save_session(self, session, response) → None`


Saves the session if it needs updates.  For the default
implementation, check :meth:`open_session`.  Instead of overriding this
method we recommend replacing the :class:`session_interface`.

.. deprecated: 1.0
    Will be removed in 2.0. Use
    ``session_interface.save_session`` instead.

:param session: the session to be saved (a
                :class:`~werkzeug.contrib.securecookie.SecureCookie`
                object)
:param response: an instance of :attr:`response_class`


- **Line:** 1091–1112
- **Complexity:** 1
- **Calls:** warn, save_session, DeprecationWarning


### `make_null_session(self) → None`


Creates a new instance of a missing session.  Instead of overriding
this method we recommend replacing the :class:`session_interface`.

.. deprecated: 1.0
    Will be removed in 2.0. Use
    ``session_interface.make_null_session`` instead.

.. versionadded:: 0.7


- **Line:** 1114–1132
- **Complexity:** 1
- **Calls:** warn, make_null_session, DeprecationWarning


### `register_blueprint(self, blueprint) → None`


Register a :class:`~flask.Blueprint` on the application. Keyword
arguments passed to this method will override the defaults set on the
blueprint.

Calls the blueprint's :meth:`~flask.Blueprint.register` method after
recording the blueprint in the application's :attr:`blueprints`.

:param blueprint: The blueprint to register.
:param url_prefix: Blueprint routes will be prefixed with this.
:param subdomain: Blueprint routes will match on this subdomain.
:param url_defaults: Blueprint routes will use these default values for
    view arguments.
:param options: Additional keyword arguments are passed to
    :class:`~flask.blueprints.BlueprintSetupState`. They can be
    accessed in :meth:`~flask.Blueprint.record` callbacks.

.. versionadded:: 0.7


- **Line:** 1135–1168
- **Complexity:** 3
- **Calls:** register, append


### `iter_blueprints(self) → None`


Iterates over all blueprints by the order they were registered.

.. versionadded:: 0.11


- **Line:** 1170–1175
- **Complexity:** 1
- **Calls:** iter


### `add_url_rule(self, rule, endpoint, view_func, provide_automatic_options) → None`


Connects a URL rule.  Works exactly like the :meth:`route`
decorator.  If a view_func is provided it will be registered with the
endpoint.

Basically this example::

    @app.route('/')
    def index():
        pass

Is equivalent to the following::

    def index():
        pass
    app.add_url_rule('/', 'index', index)

If the view_func is not provided you will need to connect the endpoint
to a view function like so::

    app.view_functions['index'] = index

Internally :meth:`route` invokes :meth:`add_url_rule` so if you want
to customize the behavior via subclassing you only need to change
this method.

For more information refer to :ref:`url-route-registrations`.

.. versionchanged:: 0.2
   `view_func` parameter added.

.. versionchanged:: 0.6
   ``OPTIONS`` is added automatically as method.

:param rule: the URL rule as string
:param endpoint: the endpoint for the registered URL rule.  Flask
                 itself assumes the name of the view function as
                 endpoint
:param view_func: the function to call when serving a request to the
                  provided endpoint
:param provide_automatic_options: controls whether the ``OPTIONS``
    method should be added automatically. This can also be controlled
    by setting the ``view_func.provide_automatic_options = False``
    before adding the rule.
:param options: the options to be forwarded to the underlying
                :class:`~werkzeug.routing.Rule` object.  A change
                to Werkzeug is handling of method options.  methods
                is a list of methods this rule should be limited
                to (``GET``, ``POST`` etc.).  By default a rule
                just listens for ``GET`` (and implicitly ``HEAD``).
                Starting with Flask 0.6, ``OPTIONS`` is implicitly
                added and handled by the standard request handling.


- **Line:** 1178–1286
- **Complexity:** 12
- **Calls:** pop, isinstance, set, url_rule_class, add, _endpoint_from_view_func, TypeError, getattr, get, upper, AssertionError


### `route(self, rule) → None`


A decorator that is used to register a view function for a
given URL rule.  This does the same thing as :meth:`add_url_rule`
but is intended for decorator usage::

    @app.route('/')
    def index():
        return 'Hello World'

For more information refer to :ref:`url-route-registrations`.

:param rule: the URL rule as string
:param endpoint: the endpoint for the registered URL rule.  Flask
                 itself assumes the name of the view function as
                 endpoint
:param options: the options to be forwarded to the underlying
                :class:`~werkzeug.routing.Rule` object.  A change
                to Werkzeug is handling of method options.  methods
                is a list of methods this rule should be limited
                to (``GET``, ``POST`` etc.).  By default a rule
                just listens for ``GET`` (and implicitly ``HEAD``).
                Starting with Flask 0.6, ``OPTIONS`` is implicitly
                added and handled by the standard request handling.


- **Line:** 1288–1318
- **Complexity:** 1
- **Calls:** pop, add_url_rule


### `decorator(f) → None`



- **Line:** 1313–1316
- **Complexity:** 1
- **Calls:** pop, add_url_rule


### `endpoint(self, endpoint) → None`


A decorator to register a function as an endpoint.
Example::

    @app.endpoint('example.endpoint')
    def example():
        return "example"

:param endpoint: the name of the endpoint


- **Line:** 1321–1336
- **Complexity:** 1
- **Calls:** none


### `decorator(f) → None`



- **Line:** 1332–1334
- **Complexity:** 1
- **Calls:** none


### `_get_exc_class_and_code(exc_class_or_code) → None`


Get the exception class being handled. For HTTP status codes
or ``HTTPException`` subclasses, return both the exception and
status code.

:param exc_class_or_code: Any exception class, or an HTTP status
    code as an integer.


- **Line:** 1339–1357
- **Complexity:** 4
- **Calls:** isinstance, issubclass


### `errorhandler(self, code_or_exception) → None`


Register a function to handle errors by code or exception class.

A decorator that is used to register a function given an
error code.  Example::

    @app.errorhandler(404)
    def page_not_found(error):
        return 'This page does not exist', 404

You can also register handlers for arbitrary exceptions::

    @app.errorhandler(DatabaseError)
    def special_exception_handler(error):
        return 'Database connection failed', 500

.. versionadded:: 0.7
    Use :meth:`register_error_handler` instead of modifying
    :attr:`error_handler_spec` directly, for application wide error
    handlers.

.. versionadded:: 0.7
   One can now additionally also register custom exception types
   that do not necessarily have to be a subclass of the
   :class:`~werkzeug.exceptions.HTTPException` class.

:param code_or_exception: the code as integer for the handler, or
                          an arbitrary exception


- **Line:** 1360–1394
- **Complexity:** 1
- **Calls:** _register_error_handler


### `decorator(f) → None`



- **Line:** 1390–1392
- **Complexity:** 1
- **Calls:** _register_error_handler


### `register_error_handler(self, code_or_exception, f) → None`


Alternative error attach function to the :meth:`errorhandler`
decorator that is more straightforward to use for non decorator
usage.

.. versionadded:: 0.7


- **Line:** 1397–1404
- **Complexity:** 1
- **Calls:** _register_error_handler


### `_register_error_handler(self, key, code_or_exception, f) → None`


:type key: None|str
:type code_or_exception: int|T<=Exception
:type f: callable


- **Line:** 1407–1429
- **Complexity:** 3
- **Calls:** isinstance, setdefault, ValueError, _get_exc_class_and_code, format, KeyError


### `template_filter(self, name) → None`


A decorator that is used to register custom template filter.
You can specify a name for the filter, otherwise the function
name will be used. Example::

  @app.template_filter()
  def reverse(s):
      return s[::-1]

:param name: the optional name of the filter, otherwise the
             function name will be used.


- **Line:** 1432–1449
- **Complexity:** 1
- **Calls:** add_template_filter


### `decorator(f) → None`



- **Line:** 1445–1447
- **Complexity:** 1
- **Calls:** add_template_filter


### `add_template_filter(self, f, name) → None`


Register a custom template filter.  Works exactly like the
:meth:`template_filter` decorator.

:param name: the optional name of the filter, otherwise the
             function name will be used.


- **Line:** 1452–1459
- **Complexity:** 2
- **Calls:** none


### `template_test(self, name) → None`


A decorator that is used to register custom template test.
You can specify a name for the test, otherwise the function
name will be used. Example::

  @app.template_test()
  def is_prime(n):
      if n == 2:
          return True
      for i in range(2, int(math.ceil(math.sqrt(n))) + 1):
          if n % i == 0:
              return False
      return True

.. versionadded:: 0.10

:param name: the optional name of the test, otherwise the
             function name will be used.


- **Line:** 1462–1486
- **Complexity:** 1
- **Calls:** add_template_test


### `decorator(f) → None`



- **Line:** 1482–1484
- **Complexity:** 1
- **Calls:** add_template_test


### `add_template_test(self, f, name) → None`


Register a custom template test.  Works exactly like the
:meth:`template_test` decorator.

.. versionadded:: 0.10

:param name: the optional name of the test, otherwise the
             function name will be used.


- **Line:** 1489–1498
- **Complexity:** 2
- **Calls:** none


### `template_global(self, name) → None`


A decorator that is used to register a custom template global function.
You can specify a name for the global function, otherwise the function
name will be used. Example::

    @app.template_global()
    def double(n):
        return 2 * n

.. versionadded:: 0.10

:param name: the optional name of the global function, otherwise the
             function name will be used.


- **Line:** 1501–1520
- **Complexity:** 1
- **Calls:** add_template_global


### `decorator(f) → None`



- **Line:** 1516–1518
- **Complexity:** 1
- **Calls:** add_template_global


### `add_template_global(self, f, name) → None`


Register a custom template global function. Works exactly like the
:meth:`template_global` decorator.

.. versionadded:: 0.10

:param name: the optional name of the global function, otherwise the
             function name will be used.


- **Line:** 1523–1532
- **Complexity:** 2
- **Calls:** none


### `before_request(self, f) → None`


Registers a function to run before each request.

For example, this can be used to open a database connection, or to load
the logged in user from the session.

The function will be called without any arguments. If it returns a
non-None value, the value is handled as if it was the return value from
the view, and further request handling is stopped.


- **Line:** 1535–1546
- **Complexity:** 1
- **Calls:** append, setdefault


### `before_first_request(self, f) → None`


Registers a function to be run before the first request to this
instance of the application.

The function will be called without any arguments and its return
value is ignored.

.. versionadded:: 0.8


- **Line:** 1549–1559
- **Complexity:** 1
- **Calls:** append


### `after_request(self, f) → None`


Register a function to be run after each request.

Your function must take one parameter, an instance of
:attr:`response_class` and return a new response object or the
same (see :meth:`process_response`).

As of Flask 0.7 this function might not be executed at the end of the
request in case an unhandled exception occurred.


- **Line:** 1562–1573
- **Complexity:** 1
- **Calls:** append, setdefault


### `teardown_request(self, f) → None`


Register a function to be run at the end of each request,
regardless of whether there was an exception or not.  These functions
are executed when the request context is popped, even if not an
actual request was performed.

Example::

    ctx = app.test_request_context()
    ctx.push()
    ...
    ctx.pop()

When ``ctx.pop()`` is executed in the above example, the teardown
functions are called just before the request context moves from the
stack of active contexts.  This becomes relevant if you are using
such constructs in tests.

Generally teardown functions must take every necessary step to avoid
that they will fail.  If they do execute code that might fail they
will have to surround the execution of these code by try/except
statements and log occurring errors.

When a teardown function was called because of an exception it will
be passed an error object.

The return values of teardown functions are ignored.

.. admonition:: Debug Note

   In debug mode Flask will not tear down a request on an exception
   immediately.  Instead it will keep it alive so that the interactive
   debugger can still access it.  This behavior can be controlled
   by the ``PRESERVE_CONTEXT_ON_EXCEPTION`` configuration variable.


- **Line:** 1576–1612
- **Complexity:** 1
- **Calls:** append, setdefault


### `teardown_appcontext(self, f) → None`


Registers a function to be called when the application context
ends.  These functions are typically also called when the request
context is popped.

Example::

    ctx = app.app_context()
    ctx.push()
    ...
    ctx.pop()

When ``ctx.pop()`` is executed in the above example, the teardown
functions are called just before the app context moves from the
stack of active contexts.  This becomes relevant if you are using
such constructs in tests.

Since a request context typically also manages an application
context it would also be called when you pop a request context.

When a teardown function was called because of an unhandled exception
it will be passed an error object. If an :meth:`errorhandler` is
registered, it will handle the exception and the teardown will not
receive it.

The return values of teardown functions are ignored.

.. versionadded:: 0.9


- **Line:** 1615–1645
- **Complexity:** 1
- **Calls:** append


### `context_processor(self, f) → None`


Registers a template context processor function.


- **Line:** 1648–1651
- **Complexity:** 1
- **Calls:** append


### `shell_context_processor(self, f) → None`


Registers a shell context processor function.

.. versionadded:: 0.11


- **Line:** 1654–1660
- **Complexity:** 1
- **Calls:** append


### `url_value_preprocessor(self, f) → None`


Register a URL value preprocessor function for all view
functions in the application. These functions will be called before the
:meth:`before_request` functions.

The function can modify the values captured from the matched url before
they are passed to the view. For example, this can be used to pop a
common language code value and place it in ``g`` rather than pass it to
every view.

The function is passed the endpoint name and values dict. The return
value is ignored.


- **Line:** 1663–1677
- **Complexity:** 1
- **Calls:** append, setdefault


### `url_defaults(self, f) → None`


Callback function for URL defaults for all view functions of the
application.  It's called with the endpoint and values and should
update the values passed in place.


- **Line:** 1680–1686
- **Complexity:** 1
- **Calls:** append, setdefault


### `_find_error_handler(self, e) → None`


Return a registered error handler for an exception in this order:
blueprint handler for a specific code, app handler for a specific code,
blueprint handler for an exception class, app handler for an exception
class, or ``None`` if a suitable handler is not found.


- **Line:** 1688–1711
- **Complexity:** 5
- **Calls:** _get_exc_class_and_code, type, get, setdefault


### `handle_http_exception(self, e) → None`


Handles an HTTP exception.  By default this will invoke the
registered error handlers and fall back to returning the
exception as response.

.. versionchanged:: 1.0.3
    ``RoutingException``, used internally for actions such as
     slash redirects during routing, is not passed to error
     handlers.

.. versionchanged:: 1.0
    Exceptions are looked up by code *and* by MRO, so
    ``HTTPExcpetion`` subclasses can be handled with a catch-all
    handler for the base ``HTTPException``.

.. versionadded:: 0.3


- **Line:** 1713–1744
- **Complexity:** 4
- **Calls:** isinstance, _find_error_handler, handler


### `trap_http_exception(self, e) → None`


Checks if an HTTP exception should be trapped or not.  By default
this will return ``False`` for all exceptions except for a bad request
key error if ``TRAP_BAD_REQUEST_ERRORS`` is set to ``True``.  It
also returns ``True`` if ``TRAP_HTTP_EXCEPTIONS`` is set to ``True``.

This is called for all HTTP exceptions raised by a view function.
If it returns ``True`` for any exception the error handler for this
exception is not called and it shows up as regular exception in the
traceback.  This is helpful for debugging implicitly raised HTTP
exceptions.

.. versionchanged:: 1.0
    Bad request errors are not trapped by default in debug mode.

.. versionadded:: 0.8


- **Line:** 1746–1779
- **Complexity:** 6
- **Calls:** isinstance


### `handle_user_exception(self, e) → None`


This method is called whenever an exception occurs that
should be handled. A special case is :class:`~werkzeug
.exceptions.HTTPException` which is forwarded to the
:meth:`handle_http_exception` method. This function will either
return a response value or reraise the exception with the same
traceback.

.. versionchanged:: 1.0
    Key errors raised from request data like ``form`` show the
    bad key in debug mode rather than a generic bad request
    message.

.. versionadded:: 0.7


- **Line:** 1781–1822
- **Complexity:** 10
- **Calls:** exc_info, isinstance, _find_error_handler, handler, handle_http_exception, reraise, trap_http_exception, get_description, format, hasattr


### `handle_exception(self, e) → None`


Handle an exception that did not have an error handler
associated with it, or that was raised from an error handler.
This always causes a 500 ``InternalServerError``.

Always sends the :data:`got_request_exception` signal.

If :attr:`propagate_exceptions` is ``True``, such as in debug
mode, the error will be re-raised so that the debugger can
display it. Otherwise, the original exception is logged, and
an :exc:`~werkzeug.exceptions.InternalServerError` is returned.

If an error handler is registered for ``InternalServerError`` or
``500``, it will be used. For consistency, the handler will
always receive the ``InternalServerError``. The original
unhandled exception is available as ``e.original_exception``.

.. note::
    Prior to Werkzeug 1.0.0, ``InternalServerError`` will not
    always have an ``original_exception`` attribute. Use
    ``getattr(e, "original_exception", None)`` to simulate the
    behavior for compatibility.

.. versionchanged:: 1.1.0
    Always passes the ``InternalServerError`` instance to the
    handler, setting ``original_exception`` to the unhandled
    error.

.. versionchanged:: 1.1.0
    ``after_request`` functions and other finalization is done
    even for the default 500 response when there is no handler.

.. versionadded:: 0.3


- **Line:** 1824–1881
- **Complexity:** 4
- **Calls:** exc_info, send, log_exception, InternalServerError, _find_error_handler, finalize_request, handler, reraise


### `log_exception(self, exc_info) → None`


Logs an exception.  This is called by :meth:`handle_exception`
if debugging is disabled and right before the handler is called.
The default implementation logs the exception as error on the
:attr:`logger`.

.. versionadded:: 0.8


- **Line:** 1883–1893
- **Complexity:** 1
- **Calls:** error


### `raise_routing_exception(self, request) → None`


Exceptions that are recording during routing are reraised with
this method.  During debug we are not reraising redirect requests
for non ``GET``, ``HEAD``, or ``OPTIONS`` requests and we're raising
a different error instead to help debug situations.

:internal:


- **Line:** 1895–1912
- **Complexity:** 4
- **Calls:** FormDataRoutingRedirect, isinstance


### `dispatch_request(self) → None`


Does the request dispatching.  Matches the URL and returns the
return value of the view or error handler.  This does not have to
be a response object.  In order to convert the return value to a
proper response object, call :func:`make_response`.

.. versionchanged:: 0.7
   This no longer does the exception handling, this code was
   moved to the new :meth:`full_dispatch_request`.


- **Line:** 1914–1936
- **Complexity:** 4
- **Calls:** raise_routing_exception, getattr, make_default_options_response


### `full_dispatch_request(self) → None`


Dispatches the request and on top of that performs request
pre and postprocessing as well as HTTP exception catching and
error handling.

.. versionadded:: 0.7


- **Line:** 1938–1953
- **Complexity:** 3
- **Calls:** try_trigger_before_first_request_functions, finalize_request, send, preprocess_request, dispatch_request, handle_user_exception


### `finalize_request(self, rv, from_error_handler) → None`


Given the return value from a view function this finalizes
the request by converting it into a response and invoking the
postprocessing functions.  This is invoked for both normal
request dispatching as well as error handlers.

Because this means that it might be called as a result of a
failure a special safe mode is available which can be enabled
with the `from_error_handler` flag.  If enabled, failures in
response processing will be logged and otherwise ignored.

:internal:


- **Line:** 1955–1978
- **Complexity:** 3
- **Calls:** make_response, process_response, send, exception


### `try_trigger_before_first_request_functions(self) → None`


Called before each request and will ensure that it triggers
the :attr:`before_first_request_funcs` and only exactly once per
application instance (which means process usually).

:internal:


- **Line:** 1980–1994
- **Complexity:** 4
- **Calls:** func


### `make_default_options_response(self) → None`


This method is called to create the default ``OPTIONS`` response.
This can be changed through subclassing to change the default
behavior of ``OPTIONS`` responses.

.. versionadded:: 0.7


- **Line:** 1996–2017
- **Complexity:** 4
- **Calls:** hasattr, response_class, update, allowed_methods, match


### `should_ignore_error(self, error) → None`


This is called to figure out if an error should be ignored
or not as far as the teardown system is concerned.  If this
function returns ``True`` then the teardown handlers will not be
passed the error.

.. versionadded:: 0.10


- **Line:** 2019–2027
- **Complexity:** 1
- **Calls:** none


### `make_response(self, rv) → None`


Convert the return value from a view function to an instance of
:attr:`response_class`.

:param rv: the return value from the view function. The view function
    must return a response. Returning ``None``, or the view ending
    without returning, is not allowed. The following types are allowed
    for ``view_rv``:

    ``str`` (``unicode`` in Python 2)
        A response object is created with the string encoded to UTF-8
        as the body.

    ``bytes`` (``str`` in Python 2)
        A response object is created with the bytes as the body.

    ``dict``
        A dictionary that will be jsonify'd before being returned.

    ``tuple``
        Either ``(body, status, headers)``, ``(body, status)``, or
        ``(body, headers)``, where ``body`` is any of the other types
        allowed here, ``status`` is a string or an integer, and
        ``headers`` is a dictionary or a list of ``(key, value)``
        tuples. If ``body`` is a :attr:`response_class` instance,
        ``status`` overwrites the exiting value and ``headers`` are
        extended.

    :attr:`response_class`
        The object is returned unchanged.

    other :class:`~werkzeug.wrappers.Response` class
        The object is coerced to :attr:`response_class`.

    :func:`callable`
        The function is called as a WSGI application. The result is
        used to create a response object.

.. versionchanged:: 0.9
   Previously a tuple was interpreted as the arguments for the
   response object.


- **Line:** 2029–2145
- **Complexity:** 15
- **Calls:** isinstance, len, TypeError, extend, response_class, jsonify, callable, force_type, format, reraise, exc_info


### `create_url_adapter(self, request) → None`


Creates a URL adapter for the given request. The URL adapter
is created at a point where the request context is not yet set
up so the request is passed explicitly.

.. versionadded:: 0.6

.. versionchanged:: 0.9
   This can now also be called without a request object when the
   URL adapter is created for the application context.

.. versionchanged:: 1.0
    :data:`SERVER_NAME` no longer implicitly enables subdomain
    matching. Use :attr:`subdomain_matching` instead.


- **Line:** 2147–2183
- **Complexity:** 5
- **Calls:** bind_to_environ, bind


### `inject_url_defaults(self, endpoint, values) → None`


Injects the URL defaults for the given endpoint directly into
the values dictionary passed.  This is used internally and
automatically called on URL building.

.. versionadded:: 0.7


- **Line:** 2185–2197
- **Complexity:** 3
- **Calls:** get, chain, func, rsplit


### `handle_url_build_error(self, error, endpoint, values) → None`


Handle :class:`~werkzeug.routing.BuildError` on :meth:`url_for`.
        


- **Line:** 2199–2217
- **Complexity:** 5
- **Calls:** exc_info, reraise, handler


### `preprocess_request(self) → None`


Called before the request is dispatched. Calls
:attr:`url_value_preprocessors` registered with the app and the
current blueprint (if any). Then calls :attr:`before_request_funcs`
registered with the app and the blueprint.

If any :meth:`before_request` handler returns a non-None value, the
value is handled as if it was the return value from the view, and
further request handling is stopped.


- **Line:** 2219–2244
- **Complexity:** 8
- **Calls:** get, chain, func


### `process_response(self, response) → None`


Can be overridden in order to modify the response object
before it's sent to the WSGI server.  By default this will
call all the :meth:`after_request` decorated functions.

.. versionchanged:: 0.5
   As of Flask 0.5 the functions registered for after request
   execution are called in reverse order of registration.

:param response: a :attr:`response_class` object.
:return: a new response object or the same, has to be an
         instance of :attr:`response_class`.


- **Line:** 2246–2270
- **Complexity:** 6
- **Calls:** chain, handler, is_null_session, save_session, reversed


### `do_teardown_request(self, exc) → None`


Called after the request is dispatched and the response is
returned, right before the request context is popped.

This calls all functions decorated with
:meth:`teardown_request`, and :meth:`Blueprint.teardown_request`
if a blueprint handled the request. Finally, the
:data:`request_tearing_down` signal is sent.

This is called by
:meth:`RequestContext.pop() <flask.ctx.RequestContext.pop>`,
which may be delayed during testing to maintain access to
resources.

:param exc: An unhandled exception raised while dispatching the
    request. Detected from the current exception information if
    not passed. Passed to each teardown function.

.. versionchanged:: 0.9
    Added the ``exc`` argument.


- **Line:** 2272–2301
- **Complexity:** 5
- **Calls:** reversed, send, get, chain, func, exc_info


### `do_teardown_appcontext(self, exc) → None`


Called right before the application context is popped.

When handling a request, the application context is popped
after the request context. See :meth:`do_teardown_request`.

This calls all functions decorated with
:meth:`teardown_appcontext`. Then the
:data:`appcontext_tearing_down` signal is sent.

This is called by
:meth:`AppContext.pop() <flask.ctx.AppContext.pop>`.

.. versionadded:: 0.9


- **Line:** 2303–2322
- **Complexity:** 3
- **Calls:** reversed, send, func, exc_info


### `app_context(self) → None`


Create an :class:`~flask.ctx.AppContext`. Use as a ``with``
block to push the context, which will make :data:`current_app`
point at this application.

An application context is automatically pushed by
:meth:`RequestContext.push() <flask.ctx.RequestContext.push>`
when handling a request, and when running a CLI command. Use
this to manually create a context outside of these situations.

::

    with app.app_context():
        init_db()

See :doc:`/appcontext`.

.. versionadded:: 0.9


- **Line:** 2324–2343
- **Complexity:** 1
- **Calls:** AppContext


### `request_context(self, environ) → None`


Create a :class:`~flask.ctx.RequestContext` representing a
WSGI environment. Use a ``with`` block to push the context,
which will make :data:`request` point at this request.

See :doc:`/reqcontext`.

Typically you should not call this from your own code. A request
context is automatically pushed by the :meth:`wsgi_app` when
handling a request. Use :meth:`test_request_context` to create
an environment and context instead of this method.

:param environ: a WSGI environment


- **Line:** 2345–2359
- **Complexity:** 1
- **Calls:** RequestContext


### `test_request_context(self) → None`


Create a :class:`~flask.ctx.RequestContext` for a WSGI
environment created from the given values. This is mostly useful
during testing, where you may want to run a function that uses
request data without dispatching a full request.

See :doc:`/reqcontext`.

Use a ``with`` block to push the context, which will make
:data:`request` point at the request for the created
environment. ::

    with test_request_context(...):
        generate_report()

When using the shell, it may be easier to push and pop the
context manually to avoid indentation. ::

    ctx = app.test_request_context(...)
    ctx.push()
    ...
    ctx.pop()

Takes the same arguments as Werkzeug's
:class:`~werkzeug.test.EnvironBuilder`, with some defaults from
the application. See the linked Werkzeug docs for most of the
available arguments. Flask-specific behavior is listed here.

:param path: URL path being requested.
:param base_url: Base URL where the app is being served, which
    ``path`` is relative to. If not given, built from
    :data:`PREFERRED_URL_SCHEME`, ``subdomain``,
    :data:`SERVER_NAME`, and :data:`APPLICATION_ROOT`.
:param subdomain: Subdomain name to append to
    :data:`SERVER_NAME`.
:param url_scheme: Scheme to use instead of
    :data:`PREFERRED_URL_SCHEME`.
:param data: The request body, either as a string or a dict of
    form keys and values.
:param json: If given, this is serialized as JSON and passed as
    ``data``. Also defaults ``content_type`` to
    ``application/json``.
:param args: other positional arguments passed to
    :class:`~werkzeug.test.EnvironBuilder`.
:param kwargs: other keyword arguments passed to
    :class:`~werkzeug.test.EnvironBuilder`.


- **Line:** 2361–2415
- **Complexity:** 1
- **Calls:** EnvironBuilder, request_context, close, get_environ


### `wsgi_app(self, environ, start_response) → None`


The actual WSGI application. This is not implemented in
:meth:`__call__` so that middlewares can be applied without
losing a reference to the app object. Instead of doing this::

    app = MyMiddleware(app)

It's a better idea to do this instead::

    app.wsgi_app = MyMiddleware(app.wsgi_app)

Then you still have the original application object around and
can continue to call methods on it.

.. versionchanged:: 0.7
    Teardown events for the request and app contexts are called
    even if an unhandled error occurs. Other events may not be
    called depending on when an error occurs during dispatch.
    See :ref:`callbacks-and-errors`.

:param environ: A WSGI environment.
:param start_response: A callable accepting a status code,
    a list of headers, and an optional exception context to
    start the response.


- **Line:** 2417–2458
- **Complexity:** 4
- **Calls:** request_context, response, should_ignore_error, auto_pop, push, full_dispatch_request, handle_exception, exc_info


### `__call__(self, environ, start_response) → None`


The WSGI server calls the Flask application object as the
WSGI application. This calls :meth:`wsgi_app` which can be
wrapped to applying middleware.


- **Line:** 2460–2464
- **Complexity:** 1
- **Calls:** wsgi_app


### `__repr__(self) → None`



- **Line:** 2466–2467
- **Complexity:** 1
- **Calls:** none



## Classes


### `Flask`


The flask object implements a WSGI application and acts as the central
object.  It is passed the name of the module or package of the
application.  Once it is created it will act as a central registry for
the view functions, the URL rules, template configuration and much more.

The name of the package is used to resolve resources from inside the
package or the folder the module is contained in depending on if the
package parameter resolves to an actual python package (a folder with
an :file:`__init__.py` file inside) or a standard module (just a ``.py`` file).

For more information about resource loading, see :func:`open_resource`.

Usually you create a :class:`Flask` instance in your main module or
in the :file:`__init__.py` file of your package like this::

    from flask import Flask
    app = Flask(__name__)

.. admonition:: About the First Parameter

    The idea of the first parameter is to give Flask an idea of what
    belongs to your application.  This name is used to find resources
    on the filesystem, can be used by extensions to improve debugging
    information and a lot more.

    So it's important what you provide there.  If you are using a single
    module, `__name__` is always the correct value.  If you however are
    using a package, it's usually recommended to hardcode the name of
    your package there.

    For example if your application is defined in :file:`yourapplication/app.py`
    you should create it with one of the two versions below::

        app = Flask('yourapplication')
        app = Flask(__name__.split('.')[0])

    Why is that?  The application will work even with `__name__`, thanks
    to how resources are looked up.  However it will make debugging more
    painful.  Certain extensions can make assumptions based on the
    import name of your application.  For example the Flask-SQLAlchemy
    extension will look for the code in your application that triggered
    an SQL query in debug mode.  If the import name is not properly set
    up, that debugging information is lost.  (For example it would only
    pick up SQL queries in `yourapplication.app` and not
    `yourapplication.views.frontend`)

.. versionadded:: 0.7
   The `static_url_path`, `static_folder`, and `template_folder`
   parameters were added.

.. versionadded:: 0.8
   The `instance_path` and `instance_relative_config` parameters were
   added.

.. versionadded:: 0.11
   The `root_path` parameter was added.

.. versionadded:: 1.0
   The ``host_matching`` and ``static_host`` parameters were added.

.. versionadded:: 1.0
   The ``subdomain_matching`` parameter was added. Subdomain
   matching needs to be enabled manually now. Setting
   :data:`SERVER_NAME` does not implicitly enable it.

:param import_name: the name of the application package
:param static_url_path: can be used to specify a different path for the
                        static files on the web.  Defaults to the name
                        of the `static_folder` folder.
:param static_folder: The folder with static files that is served at
    ``static_url_path``. Relative to the application ``root_path``
    or an absolute path. Defaults to ``'static'``.
:param static_host: the host to use when adding the static route.
    Defaults to None. Required when using ``host_matching=True``
    with a ``static_folder`` configured.
:param host_matching: set ``url_map.host_matching`` attribute.
    Defaults to False.
:param subdomain_matching: consider the subdomain relative to
    :data:`SERVER_NAME` when matching routes. Defaults to False.
:param template_folder: the folder that contains the templates that should
                        be used by the application.  Defaults to
                        ``'templates'`` folder in the root path of the
                        application.
:param instance_path: An alternative instance path for the application.
                      By default the folder ``'instance'`` next to the
                      package or module is assumed to be the instance
                      path.
:param instance_relative_config: if set to ``True`` relative filenames
                                 for loading the config are assumed to
                                 be relative to the instance path instead
                                 of the application root.
:param root_path: Flask by default will automatically calculate the path
                  to the root of the application.  In certain situations
                  this cannot be achieved (for instance if the package
                  is a Python 3 namespace package) and needs to be
                  manually defined.


- **Bases:** _PackageBoundObject
- **Methods:** __init__, name, propagate_exceptions, preserve_context_on_exception, logger, jinja_env, got_first_request, make_config, auto_find_instance_path, open_instance_resource, templates_auto_reload, create_jinja_environment, create_global_jinja_loader, select_jinja_autoescape, update_template_context, make_shell_context, debug, run, test_client, test_cli_runner, open_session, save_session, make_null_session, register_blueprint, iter_blueprints, add_url_rule, route, endpoint, _get_exc_class_and_code, errorhandler, register_error_handler, _register_error_handler, template_filter, add_template_filter, template_test, add_template_test, template_global, add_template_global, before_request, before_first_request, after_request, teardown_request, teardown_appcontext, context_processor, shell_context_processor, url_value_preprocessor, url_defaults, _find_error_handler, handle_http_exception, trap_http_exception, handle_user_exception, handle_exception, log_exception, raise_routing_exception, dispatch_request, full_dispatch_request, finalize_request, try_trigger_before_first_request_functions, make_default_options_response, should_ignore_error, make_response, create_url_adapter, inject_url_defaults, handle_url_build_error, preprocess_request, process_response, do_teardown_request, do_teardown_appcontext, app_context, request_context, test_request_context, wsgi_app, __call__, __repr__

