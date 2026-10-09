# Module: `src/flask/cli.py`

**Path:** `C:\temp\flask\src\flask\cli.py`
**Lines:** 971
**Avg Complexity:** 4.3


## Description

flask.cli
~~~~~~~~~

A simple command line application to run flask apps.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `__future__.print_function`

- `ast`

- `inspect`

- `os`

- `platform`

- `re`

- `sys`

- `traceback`

- `functools.update_wrapper`

- `operator.attrgetter`

- `threading.Lock`

- `threading.Thread`

- `click`

- `werkzeug.utils.import_string`

- `_compat.getargspec`

- `_compat.itervalues`

- `_compat.reraise`

- `_compat.text_type`

- `globals.current_app`

- `helpers.get_debug_flag`

- `helpers.get_env`

- `helpers.get_load_dotenv`

- `dotenv`

- `ssl`

- `Flask`

- `Flask`

- `werkzeug`

- `__version__`

- `werkzeug.serving.run_simple`

- `code`

- `globals._app_ctx_stack`

- `pkg_resources`

- `OpenSSL`



## Functions


### `find_best_app(script_info, module) → None`


Given a module instance this tries to find the best possible
application in the module or raises an exception.


- **Line:** 52–100
- **Complexity:** 12
- **Calls:** NoAppException, getattr, isinstance, len, isfunction, format, itervalues, call_factory, _called_with_wrong_args


### `call_factory(script_info, app_factory, arguments) → None`


Takes an app factory, a ``script_info` object and  optionally a tuple
of arguments. Checks for the existence of a script_info argument and calls
the app_factory depending on that and the arguments provided.


- **Line:** 103–119
- **Complexity:** 6
- **Calls:** getargspec, app_factory, len


### `_called_with_wrong_args(factory) → None`


Check whether calling a function raised a ``TypeError`` because
the call failed or because something in the factory raised the
error.

:param factory: the factory function that was called
:return: true if the call failed


- **Line:** 122–145
- **Complexity:** 3
- **Calls:** exc_info


### `find_app_by_string(script_info, module, app_name) → None`


Checks if the given string is a variable name or a function. If it is a
function, it checks for specified arguments and whether it takes a
``script_info`` argument and calls the function with the appropriate
arguments.


- **Line:** 148–204
- **Complexity:** 9
- **Calls:** match, groups, isfunction, isinstance, NoAppException, getattr, format, call_factory, literal_eval, _called_with_wrong_args


### `prepare_import(path) → None`


Given a filename this will try to calculate the python path, add it
to the search path and return the actual module name that is expected.


- **Line:** 207–233
- **Complexity:** 6
- **Calls:** realpath, splitext, join, basename, dirname, split, append, insert, exists


### `locate_app(script_info, module_name, app_name, raise_if_not_found) → None`



- **Line:** 236–259
- **Complexity:** 5
- **Calls:** __import__, find_best_app, find_app_by_string, NoAppException, exc_info, format, format_exc


### `get_version(ctx, param, value) → None`



- **Line:** 262–279
- **Complexity:** 3
- **Calls:** echo, exit, python_version


### `__init__(self, loader, use_eager_loading) → None`



- **Line:** 299–307
- **Complexity:** 1
- **Calls:** Lock, _load_unlocked, _load_in_background


### `_load_in_background(self) → None`



- **Line:** 309–319
- **Complexity:** 1
- **Calls:** Thread, start, _load_unlocked, exc_info


### `_load_app() → None`



- **Line:** 310–316
- **Complexity:** 1
- **Calls:** _load_unlocked, exc_info


### `_flush_bg_loading_exception(self) → None`



- **Line:** 321–326
- **Complexity:** 2
- **Calls:** reraise


### `_load_unlocked(self) → None`



- **Line:** 328–332
- **Complexity:** 1
- **Calls:** loader


### `__call__(self, environ, start_response) → None`



- **Line:** 334–344
- **Complexity:** 3
- **Calls:** _flush_bg_loading_exception, _app, rv, _load_unlocked


### `__init__(self, app_import_path, create_app, set_debug_flag) → None`



- **Line:** 356–366
- **Complexity:** 1
- **Calls:** get


### `load_app(self) → None`


Loads the Flask app (if not yet loaded) and returns it.  Calling
this multiple times will just result in the already loaded app to
be returned.


- **Line:** 368–410
- **Complexity:** 8
- **Calls:** call_factory, NoAppException, get_debug_flag, prepare_import, locate_app, split


### `with_appcontext(f) → None`


Wraps a callback so that it's guaranteed to be executed with the
script's application context.  If callbacks are registered directly
to the ``app.cli`` object then they are wrapped with this function
by default unless it's disabled.


- **Line:** 416–428
- **Complexity:** 1
- **Calls:** update_wrapper, app_context, invoke, load_app, ensure_object


### `decorator(__ctx) → None`



- **Line:** 424–426
- **Complexity:** 1
- **Calls:** app_context, invoke, load_app, ensure_object


### `command(self) → None`


This works exactly like the method of the same name on a regular
:class:`click.Group` but it wraps callbacks in :func:`with_appcontext`
unless it's disabled by passing ``with_appcontext=False``.


- **Line:** 439–451
- **Complexity:** 1
- **Calls:** pop, with_appcontext, command


### `decorator(f) → None`



- **Line:** 446–449
- **Complexity:** 1
- **Calls:** with_appcontext, command


### `group(self) → None`


This works exactly like the method of the same name on a regular
:class:`click.Group` but it defaults the group class to
:class:`AppGroup`.


- **Line:** 453–459
- **Complexity:** 1
- **Calls:** setdefault, group


### `__init__(self, add_default_commands, create_app, add_version_option, load_dotenv, set_debug_flag) → None`



- **Line:** 487–511
- **Complexity:** 1
- **Calls:** list, __init__, append, add_command, pop


### `_load_plugin_commands(self) → None`



- **Line:** 513–524
- **Complexity:** 4
- **Calls:** iter_entry_points, add_command, load


### `get_command(self, ctx, name) → None`



- **Line:** 526–546
- **Complexity:** 4
- **Calls:** _load_plugin_commands, get_command, ensure_object, load_app


### `list_commands(self, ctx) → None`



- **Line:** 548–565
- **Complexity:** 2
- **Calls:** _load_plugin_commands, set, ensure_object, sorted, list_commands, update, print_exc, load_app


### `main(self) → None`



- **Line:** 567–586
- **Complexity:** 3
- **Calls:** get_load_dotenv, get, setdefault, main, load_dotenv, ScriptInfo, super


### `_path_is_ancestor(path, other) → None`


Take ``other`` and remove the length of ``path`` from it. Then join it
to ``path``. If it is the original value, ``path`` is an ancestor of
``other``.


- **Line:** 589–593
- **Complexity:** 1
- **Calls:** join, lstrip, len


### `load_dotenv(path) → None`


Load "dotenv" files in order of precedence to set environment variables.

If an env var is already set it is not overwritten, so earlier files in the
list are preferred over later files.

Changes the current working directory to the location of the first file
found, with the assumption that it is in the top level project directory
and will be where the Python path should import local packages from.

This is a no-op if `python-dotenv`_ is not installed.

.. _python-dotenv: https://github.com/theskumar/python-dotenv#readme

:param path: Load the file at this location instead of searching.
:return: ``True`` if a file was loaded.

.. versionchanged:: 1.1.0
    Returns ``False`` when python-dotenv is not installed, or when
    the given path isn't a file.

.. versionadded:: 1.0


- **Line:** 596–654
- **Complexity:** 12
- **Calls:** isfile, find_dotenv, load_dotenv, chdir, secho, dirname, getcwd


### `show_server_banner(env, debug, app_import_path, eager_loading) → None`


Show extra startup messages the first time the server is run,
ignoring the reloader.


- **Line:** 657–683
- **Complexity:** 7
- **Calls:** echo, get, format, secho


### `__init__(self) → None`



- **Line:** 694–695
- **Complexity:** 1
- **Calls:** Path


### `convert(self, value, param, ctx) → None`



- **Line:** 697–729
- **Complexity:** 2
- **Calls:** BadParameter, path_type, lower, import_string, isinstance, STRING


### `_validate_key(ctx, param, value) → None`


The ``--key`` option must be specified when ``--cert`` is a file.
Modifies the ``cert`` param to be a ``(cert, key)`` pair if needed.


- **Line:** 732–764
- **Complexity:** 10
- **Calls:** get, isinstance, BadParameter


### `convert(self, value, param, ctx) → None`



- **Line:** 773–776
- **Complexity:** 2
- **Calls:** split_envvar_value, super, super_convert


### `run_command(info, host, port, reload, debugger, eager_loading, with_threads, cert, extra_files) → None`


Run a local development server.

This server is for development purposes only. It does not provide
the stability, security, or performance of production WSGI servers.

The reloader and debugger are enabled by default if
FLASK_ENV=development or FLASK_DEBUG=1.


- **Line:** 825–861
- **Complexity:** 4
- **Calls:** command, option, get_debug_flag, show_server_banner, DispatchingApp, run_simple, get_env, CertParamType, Path, SeparatedPathType, format


### `shell_command() → None`


Run an interactive Python shell in the context of a given
Flask application.  The application will populate the default
namespace of this shell according to it's configuration.

This is useful for executing small snippets of management code
without having to manually configure the application.


- **Line:** 866–896
- **Complexity:** 3
- **Calls:** command, get, update, interact, isfile, make_shell_context, open, eval, compile, read


### `routes_command(sort, all_methods) → None`


Show all registered routes with endpoints and methods.


- **Line:** 912–942
- **Complexity:** 12
- **Calls:** command, option, list, set, format, echo, zip, iter_rules, sorted, join, max, strip, Choice, len, rstrip, attrgetter


### `main(as_module) → None`



- **Line:** 965–967
- **Complexity:** 3
- **Calls:** main



## Classes


### `NoAppException`


Raised if an application cannot be found or loaded.


- **Bases:** click.UsageError
- **Methods:** none


### `DispatchingApp`


Special application that dispatches to a Flask application which
is imported by name in a background thread.  If an error happens
it is recorded and shown as part of the WSGI handling which in case
of the Werkzeug debugger means that it shows up in the browser.


- **Bases:** object
- **Methods:** __init__, _load_in_background, _flush_bg_loading_exception, _load_unlocked, __call__


### `ScriptInfo`


Helper object to deal with Flask applications.  This is usually not
necessary to interface with as it's used internally in the dispatching
to click.  In future versions of Flask this object will most likely play
a bigger role.  Typically it's created automatically by the
:class:`FlaskGroup` but you can also manually create it and pass it
onwards as click object.


- **Bases:** object
- **Methods:** __init__, load_app


### `AppGroup`


This works similar to a regular click :class:`~click.Group` but it
changes the behavior of the :meth:`command` decorator so that it
automatically wraps the functions in :func:`with_appcontext`.

Not to be confused with :class:`FlaskGroup`.


- **Bases:** click.Group
- **Methods:** command, group


### `FlaskGroup`


Special subclass of the :class:`AppGroup` group that supports
loading more commands from the configured Flask app.  Normally a
developer does not have to interface with this class but there are
some very advanced use cases for which it makes sense to create an
instance of this.

For information as of why this is useful see :ref:`custom-scripts`.

:param add_default_commands: if this is True then the default run and
    shell commands will be added.
:param add_version_option: adds the ``--version`` option.
:param create_app: an optional callback that is passed the script info and
    returns the loaded app.
:param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
    files to set environment variables. Will also change the working
    directory to the directory containing the first file found.
:param set_debug_flag: Set the app's debug flag based on the active
    environment

.. versionchanged:: 1.0
    If installed, python-dotenv will be used to load environment variables
    from :file:`.env` and :file:`.flaskenv` files.


- **Bases:** AppGroup
- **Methods:** __init__, _load_plugin_commands, get_command, list_commands, main


### `CertParamType`


Click option type for the ``--cert`` option. Allows either an
existing file, the string ``'adhoc'``, or an import for a
:class:`~ssl.SSLContext` object.


- **Bases:** click.ParamType
- **Methods:** __init__, convert


### `SeparatedPathType`


Click option type that accepts a list of values separated by the
OS's path separator (``:``, ``;`` on Windows). Each value is
validated as a :class:`click.Path` type.


- **Bases:** click.Path
- **Methods:** convert

