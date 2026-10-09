# Module: `src/flask/blueprints.py`

**Path:** `C:\temp\flask\src\flask\blueprints.py`
**Lines:** 569
**Avg Complexity:** 1.6


## Description

flask.blueprints
~~~~~~~~~~~~~~~~

Blueprints are the recommended way to implement larger or more
pluggable applications in Flask 0.7 and later.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `functools.update_wrapper`

- `helpers._endpoint_from_view_func`

- `helpers._PackageBoundObject`

- `warnings.warn`



## Functions


### `__init__(self, blueprint, app, options, first_registration) → None`



- **Line:** 28–63
- **Complexity:** 2
- **Calls:** get, dict, update


### `add_url_rule(self, rule, endpoint, view_func) → None`


A helper method to register a rule (and optionally a view function)
to the application.  The endpoint is automatically prefixed with the
blueprint's name.


- **Line:** 65–87
- **Complexity:** 6
- **Calls:** setdefault, add_url_rule, _endpoint_from_view_func, dict, join, pop, rstrip, lstrip


### `__init__(self, name, import_name, static_folder, static_url_path, template_folder, url_prefix, subdomain, url_defaults, root_path, cli_group) → None`



- **Line:** 168–193
- **Complexity:** 2
- **Calls:** __init__


### `record(self, func) → None`


Registers a function that is called when the blueprint is
registered on the application.  This function is called with the
state as argument as returned by the :meth:`make_setup_state`
method.


- **Line:** 195–211
- **Complexity:** 3
- **Calls:** append, warn, Warning


### `record_once(self, func) → None`


Works like :meth:`record` but wraps the function in another
function that will ensure the function is only called once.  If the
blueprint is registered a second time on the application, the
function passed is not called.


- **Line:** 213–224
- **Complexity:** 1
- **Calls:** record, update_wrapper, func


### `wrapper(state) → None`



- **Line:** 220–222
- **Complexity:** 1
- **Calls:** func


### `make_setup_state(self, app, options, first_registration) → None`


Creates an instance of :meth:`~flask.blueprints.BlueprintSetupState`
object that is later passed to the register callback functions.
Subclasses can override this to return a subclass of the setup state.


- **Line:** 226–231
- **Complexity:** 1
- **Calls:** BlueprintSetupState


### `register(self, app, options, first_registration) → None`


Called by :meth:`Flask.register_blueprint` to register all views
and callbacks registered on the blueprint with the application. Creates
a :class:`.BlueprintSetupState` and calls each :meth:`record` callback
with it.

:param app: The application this blueprint is being registered with.
:param options: Keyword arguments forwarded from
    :meth:`~Flask.register_blueprint`.
:param first_registration: Whether this is the first time this
    blueprint has been registered on the application.


- **Line:** 233–270
- **Complexity:** 6
- **Calls:** make_setup_state, get, add_url_rule, deferred, update, add_command


### `route(self, rule) → None`


Like :meth:`Flask.route` but for a blueprint.  The endpoint for the
:func:`url_for` function is prefixed with the name of the blueprint.


- **Line:** 272–282
- **Complexity:** 1
- **Calls:** pop, add_url_rule


### `decorator(f) → None`



- **Line:** 277–280
- **Complexity:** 1
- **Calls:** pop, add_url_rule


### `add_url_rule(self, rule, endpoint, view_func) → None`


Like :meth:`Flask.add_url_rule` but for a blueprint.  The endpoint for
the :func:`url_for` function is prefixed with the name of the blueprint.


- **Line:** 284–294
- **Complexity:** 6
- **Calls:** record, hasattr, add_url_rule


### `endpoint(self, endpoint) → None`


Like :meth:`Flask.endpoint` but for a blueprint.  This does not
prefix the endpoint with the blueprint name, this has to be done
explicitly by the user of this method.  If the endpoint is prefixed
with a `.` it will be registered to the current blueprint, otherwise
it's an application independent endpoint.


- **Line:** 296–311
- **Complexity:** 1
- **Calls:** record_once


### `decorator(f) → None`



- **Line:** 304–309
- **Complexity:** 1
- **Calls:** record_once


### `register_endpoint(state) → None`



- **Line:** 305–306
- **Complexity:** 1
- **Calls:** none


### `app_template_filter(self, name) → None`


Register a custom template filter, available application wide.  Like
:meth:`Flask.template_filter` but for a blueprint.

:param name: the optional name of the filter, otherwise the
             function name will be used.


- **Line:** 313–325
- **Complexity:** 1
- **Calls:** add_app_template_filter


### `decorator(f) → None`



- **Line:** 321–323
- **Complexity:** 1
- **Calls:** add_app_template_filter


### `add_app_template_filter(self, f, name) → None`


Register a custom template filter, available application wide.  Like
:meth:`Flask.add_template_filter` but for a blueprint.  Works exactly
like the :meth:`app_template_filter` decorator.

:param name: the optional name of the filter, otherwise the
             function name will be used.


- **Line:** 327–339
- **Complexity:** 1
- **Calls:** record_once


### `register_template(state) → None`



- **Line:** 336–337
- **Complexity:** 1
- **Calls:** none


### `app_template_test(self, name) → None`


Register a custom template test, available application wide.  Like
:meth:`Flask.template_test` but for a blueprint.

.. versionadded:: 0.10

:param name: the optional name of the test, otherwise the
             function name will be used.


- **Line:** 341–355
- **Complexity:** 1
- **Calls:** add_app_template_test


### `decorator(f) → None`



- **Line:** 351–353
- **Complexity:** 1
- **Calls:** add_app_template_test


### `add_app_template_test(self, f, name) → None`


Register a custom template test, available application wide.  Like
:meth:`Flask.add_template_test` but for a blueprint.  Works exactly
like the :meth:`app_template_test` decorator.

.. versionadded:: 0.10

:param name: the optional name of the test, otherwise the
             function name will be used.


- **Line:** 357–371
- **Complexity:** 1
- **Calls:** record_once


### `register_template(state) → None`



- **Line:** 368–369
- **Complexity:** 1
- **Calls:** none


### `app_template_global(self, name) → None`


Register a custom template global, available application wide.  Like
:meth:`Flask.template_global` but for a blueprint.

.. versionadded:: 0.10

:param name: the optional name of the global, otherwise the
             function name will be used.


- **Line:** 373–387
- **Complexity:** 1
- **Calls:** add_app_template_global


### `decorator(f) → None`



- **Line:** 383–385
- **Complexity:** 1
- **Calls:** add_app_template_global


### `add_app_template_global(self, f, name) → None`


Register a custom template global, available application wide.  Like
:meth:`Flask.add_template_global` but for a blueprint.  Works exactly
like the :meth:`app_template_global` decorator.

.. versionadded:: 0.10

:param name: the optional name of the global, otherwise the
             function name will be used.


- **Line:** 389–403
- **Complexity:** 1
- **Calls:** record_once


### `register_template(state) → None`



- **Line:** 400–401
- **Complexity:** 1
- **Calls:** none


### `before_request(self, f) → None`


Like :meth:`Flask.before_request` but for a blueprint.  This function
is only executed before each request that is handled by a function of
that blueprint.


- **Line:** 405–413
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `before_app_request(self, f) → None`


Like :meth:`Flask.before_request`.  Such a function is executed
before each request, even if outside of a blueprint.


- **Line:** 415–422
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `before_app_first_request(self, f) → None`


Like :meth:`Flask.before_first_request`.  Such a function is
executed before the first request to the application.


- **Line:** 424–429
- **Complexity:** 1
- **Calls:** record_once, append


### `after_request(self, f) → None`


Like :meth:`Flask.after_request` but for a blueprint.  This function
is only executed after each request that is handled by a function of
that blueprint.


- **Line:** 431–439
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `after_app_request(self, f) → None`


Like :meth:`Flask.after_request` but for a blueprint.  Such a function
is executed after each request, even if outside of the blueprint.


- **Line:** 441–448
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `teardown_request(self, f) → None`


Like :meth:`Flask.teardown_request` but for a blueprint.  This
function is only executed when tearing down requests handled by a
function of that blueprint.  Teardown request functions are executed
when the request context is popped, even when no actual request was
performed.


- **Line:** 450–460
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `teardown_app_request(self, f) → None`


Like :meth:`Flask.teardown_request` but for a blueprint.  Such a
function is executed when tearing down each request, even if outside of
the blueprint.


- **Line:** 462–470
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `context_processor(self, f) → None`


Like :meth:`Flask.context_processor` but for a blueprint.  This
function is only executed for requests handled by a blueprint.


- **Line:** 472–481
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `app_context_processor(self, f) → None`


Like :meth:`Flask.context_processor` but for a blueprint.  Such a
function is executed each request, even if outside of the blueprint.


- **Line:** 483–490
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `app_errorhandler(self, code) → None`


Like :meth:`Flask.errorhandler` but for a blueprint.  This
handler is used for all requests, even if outside of the blueprint.


- **Line:** 492–501
- **Complexity:** 1
- **Calls:** record_once, errorhandler


### `decorator(f) → None`



- **Line:** 497–499
- **Complexity:** 1
- **Calls:** record_once, errorhandler


### `url_value_preprocessor(self, f) → None`


Registers a function as URL value preprocessor for this
blueprint.  It's called before the view functions are called and
can modify the url values provided.


- **Line:** 503–511
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `url_defaults(self, f) → None`


Callback function for URL defaults for this blueprint.  It's called
with the endpoint and values and should update the values passed
in place.


- **Line:** 513–521
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `app_url_value_preprocessor(self, f) → None`


Same as :meth:`url_value_preprocessor` but application wide.
        


- **Line:** 523–529
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `app_url_defaults(self, f) → None`


Same as :meth:`url_defaults` but application wide.
        


- **Line:** 531–537
- **Complexity:** 1
- **Calls:** record_once, append, setdefault


### `errorhandler(self, code_or_exception) → None`


Registers an error handler that becomes active for this blueprint
only.  Please be aware that routing does not happen local to a
blueprint so an error handler for 404 usually is not handled by
a blueprint unless it is caused inside a view function.  Another
special case is the 500 internal server error which is always looked
up from the application.

Otherwise works as the :meth:`~flask.Flask.errorhandler` decorator
of the :class:`~flask.Flask` object.


- **Line:** 539–557
- **Complexity:** 1
- **Calls:** record_once, _register_error_handler


### `decorator(f) → None`



- **Line:** 551–555
- **Complexity:** 1
- **Calls:** record_once, _register_error_handler


### `register_error_handler(self, code_or_exception, f) → None`


Non-decorator version of the :meth:`errorhandler` error attach
function, akin to the :meth:`~flask.Flask.register_error_handler`
application-wide function of the :class:`~flask.Flask` object but
for error handlers limited to this blueprint.

.. versionadded:: 0.11


- **Line:** 559–569
- **Complexity:** 1
- **Calls:** record_once, _register_error_handler



## Classes


### `BlueprintSetupState`


Temporary holder object for registering a blueprint with the
application.  An instance of this class is created by the
:meth:`~flask.Blueprint.make_setup_state` method and later passed
to all register callback functions.


- **Bases:** object
- **Methods:** __init__, add_url_rule


### `Blueprint`


Represents a blueprint, a collection of routes and other
app-related functions that can be registered on a real application
later.

A blueprint is an object that allows defining application functions
without requiring an application object ahead of time. It uses the
same decorators as :class:`~flask.Flask`, but defers the need for an
application by recording them for later registration.

Decorating a function with a blueprint creates a deferred function
that is called with :class:`~flask.blueprints.BlueprintSetupState`
when the blueprint is registered on an application.

See :ref:`blueprints` for more information.

.. versionchanged:: 1.1.0
    Blueprints have a ``cli`` group to register nested CLI commands.
    The ``cli_group`` parameter controls the name of the group under
    the ``flask`` command.

.. versionadded:: 0.7

:param name: The name of the blueprint. Will be prepended to each
    endpoint name.
:param import_name: The name of the blueprint package, usually
    ``__name__``. This helps locate the ``root_path`` for the
    blueprint.
:param static_folder: A folder with static files that should be
    served by the blueprint's static route. The path is relative to
    the blueprint's root path. Blueprint static files are disabled
    by default.
:param static_url_path: The url to serve static files from.
    Defaults to ``static_folder``. If the blueprint does not have
    a ``url_prefix``, the app's static route will take precedence,
    and the blueprint's static files won't be accessible.
:param template_folder: A folder with templates that should be added
    to the app's template search path. The path is relative to the
    blueprint's root path. Blueprint templates are disabled by
    default. Blueprint templates have a lower precedence than those
    in the app's templates folder.
:param url_prefix: A path to prepend to all of the blueprint's URLs,
    to make them distinct from the rest of the app's routes.
:param subdomain: A subdomain that blueprint routes will match on by
    default.
:param url_defaults: A dict of default values that blueprint routes
    will receive by default.
:param root_path: By default, the blueprint will automatically this
    based on ``import_name``. In certain situations this automatic
    detection can fail, so the path can be specified manually
    instead.


- **Bases:** _PackageBoundObject
- **Methods:** __init__, record, record_once, make_setup_state, register, route, add_url_rule, endpoint, app_template_filter, add_app_template_filter, app_template_test, add_app_template_test, app_template_global, add_app_template_global, before_request, before_app_request, before_app_first_request, after_request, after_app_request, teardown_request, teardown_app_request, context_processor, app_context_processor, app_errorhandler, url_value_preprocessor, url_defaults, app_url_value_preprocessor, app_url_defaults, errorhandler, register_error_handler

