# Module: `src/flask/ctx.py`

**Path:** `C:\temp\flask\src\flask\ctx.py`
**Lines:** 475
**Avg Complexity:** 2.4


## Description

flask.ctx
~~~~~~~~~

Implements the objects required to keep the context.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `sys`

- `functools.update_wrapper`

- `werkzeug.exceptions.HTTPException`

- `_compat.BROKEN_PYPY_CTXMGR_EXIT`

- `_compat.reraise`

- `globals._app_ctx_stack`

- `globals._request_ctx_stack`

- `signals.appcontext_popped`

- `signals.appcontext_pushed`



## Functions


### `get(self, name, default) → None`


Get an attribute by name, or a default value. Like
:meth:`dict.get`.

:param name: Name of attribute to get.
:param default: Value to return if the attribute is not present.

.. versionadded:: 0.10


- **Line:** 48–57
- **Complexity:** 1
- **Calls:** get


### `pop(self, name, default) → None`


Get and remove an attribute by name. Like :meth:`dict.pop`.

:param name: Name of attribute to pop.
:param default: Value to return if the attribute is not present,
    instead of raise a ``KeyError``.

.. versionadded:: 0.11


- **Line:** 59–71
- **Complexity:** 8
- **Calls:** pop


### `setdefault(self, name, default) → None`


Get the value of an attribute if it is present, otherwise
set and return a default value. Like :meth:`dict.setdefault`.

:param name: Name of attribute to get.
:param: default: Value to set and return if the attribute is not
    present.

.. versionadded:: 0.11


- **Line:** 73–83
- **Complexity:** 1
- **Calls:** setdefault


### `__contains__(self, item) → None`



- **Line:** 85–86
- **Complexity:** 1
- **Calls:** none


### `__iter__(self) → None`



- **Line:** 88–89
- **Complexity:** 1
- **Calls:** iter


### `__repr__(self) → None`



- **Line:** 91–95
- **Complexity:** 1
- **Calls:** __repr__


### `after_this_request(f) → None`


Executes a function after this request.  This is useful to modify
response objects.  The function is passed the response object and has
to return the same or a new one.

Example::

    @app.route('/')
    def index():
        @after_this_request
        def add_header(response):
            response.headers['X-Foo'] = 'Parachute'
            return response
        return 'Hello World!'

This is more useful if a function other than the view function wants to
modify a response.  For instance think of a decorator that wants to add
some headers without converting the return value into a response object.

.. versionadded:: 0.9


- **Line:** 98–120
- **Complexity:** 1
- **Calls:** append


### `copy_current_request_context(f) → None`


A helper function that decorates a function to retain the current
request context.  This is useful when working with greenlets.  The moment
the function is decorated a copy of the request context is created and
then pushed when the function is called.  The current session is also
included in the copied request context.

Example::

    import gevent
    from flask import copy_current_request_context

    @app.route('/')
    def index():
        @copy_current_request_context
        def do_some_work():
            # do some work here, it can access flask.request or
            # flask.session like you would otherwise in the view function.
            ...
        gevent.spawn(do_some_work)
        return 'Regular response'

.. versionadded:: 0.10


- **Line:** 123–160
- **Complexity:** 2
- **Calls:** copy, update_wrapper, RuntimeError, f


### `wrapper() → None`



- **Line:** 156–158
- **Complexity:** 1
- **Calls:** f


### `has_request_context() → None`


If you have code that wants to test if a request context is there or
not this function can be used.  For instance, you may want to take advantage
of request information if the request object is available, but fail
silently if it is unavailable.

::

    class User(db.Model):

        def __init__(self, username, remote_addr=None):
            self.username = username
            if remote_addr is None and has_request_context():
                remote_addr = request.remote_addr
            self.remote_addr = remote_addr

Alternatively you can also just test any of the context bound objects
(such as :class:`request` or :class:`g`) for truthness::

    class User(db.Model):

        def __init__(self, username, remote_addr=None):
            self.username = username
            if remote_addr is None and request:
                remote_addr = request.remote_addr
            self.remote_addr = remote_addr

.. versionadded:: 0.7


- **Line:** 163–192
- **Complexity:** 1
- **Calls:** none


### `has_app_context() → None`


Works like :func:`has_request_context` but for the application
context.  You can also just do a boolean check on the
:data:`current_app` object instead.

.. versionadded:: 0.9


- **Line:** 195–202
- **Complexity:** 1
- **Calls:** none


### `__init__(self, app) → None`



- **Line:** 214–221
- **Complexity:** 3
- **Calls:** create_url_adapter, app_ctx_globals_class


### `push(self) → None`


Binds the app context to the current context.


- **Line:** 223–229
- **Complexity:** 9
- **Calls:** hasattr, push, send, exc_clear


### `pop(self, exc) → None`


Pops the app context.


- **Line:** 231–242
- **Complexity:** 8
- **Calls:** send, pop, do_teardown_appcontext, exc_info


### `__enter__(self) → None`



- **Line:** 244–246
- **Complexity:** 1
- **Calls:** push


### `__exit__(self, exc_type, exc_value, tb) → None`



- **Line:** 248–252
- **Complexity:** 3
- **Calls:** pop, reraise


### `__init__(self, app, environ, request, session) → None`



- **Line:** 285–315
- **Complexity:** 3
- **Calls:** request_class, create_url_adapter


### `g(self) → None`



- **Line:** 318–319
- **Complexity:** 1
- **Calls:** none


### `g(self, value) → None`



- **Line:** 322–323
- **Complexity:** 1
- **Calls:** none


### `copy(self) → None`


Creates a copy of this request context with the same request object.
This can be used to move a request context to a different greenlet.
Because the actual request object is the same this cannot be used to
move a request context to a different thread unless access to the
request object is locked.

.. versionadded:: 0.10

.. versionchanged:: 1.1
   The current session object is used instead of reloading the original
   data. This prevents `flask.session` pointing to an out-of-date object.


- **Line:** 325–343
- **Complexity:** 1
- **Calls:** __class__


### `match_request(self) → None`


Can be overridden by a subclass to hook into the matching
of the request.


- **Line:** 345–353
- **Complexity:** 2
- **Calls:** match


### `push(self) → None`


Binds the request context to the current context.


- **Line:** 355–396
- **Complexity:** 9
- **Calls:** hasattr, push, pop, app_context, append, exc_clear, open_session, match_request, make_null_session


### `pop(self, exc) → None`


Pops the request context and unbinds it by doing that.  This will
also trigger the execution of functions registered by the
:meth:`~flask.Flask.teardown_request` decorator.

.. versionchanged:: 0.9
   Added the `exc` argument.


- **Line:** 398–443
- **Complexity:** 8
- **Calls:** pop, do_teardown_request, hasattr, getattr, exc_clear, request_close, exc_info


### `auto_pop(self, exc) → None`



- **Line:** 445–452
- **Complexity:** 4
- **Calls:** get, pop


### `__enter__(self) → None`



- **Line:** 454–456
- **Complexity:** 1
- **Calls:** push


### `__exit__(self, exc_type, exc_value, tb) → None`



- **Line:** 458–467
- **Complexity:** 3
- **Calls:** auto_pop, reraise


### `__repr__(self) → None`



- **Line:** 469–475
- **Complexity:** 1
- **Calls:** none



## Classes


### `_AppCtxGlobals`


A plain object. Used as a namespace for storing data during an
application context.

Creating an app context automatically creates this object, which is
made available as the :data:`g` proxy.

.. describe:: 'key' in g

    Check whether an attribute is present.

    .. versionadded:: 0.10

.. describe:: iter(g)

    Return an iterator over the attribute names.

    .. versionadded:: 0.10


- **Bases:** object
- **Methods:** get, pop, setdefault, __contains__, __iter__, __repr__


### `AppContext`


The application context binds an application object implicitly
to the current thread or greenlet, similar to how the
:class:`RequestContext` binds request information.  The application
context is also implicitly created if a request context is created
but the application is not on top of the individual application
context.


- **Bases:** object
- **Methods:** __init__, push, pop, __enter__, __exit__


### `RequestContext`


The request context contains all request relevant information.  It is
created at the beginning of the request and pushed to the
`_request_ctx_stack` and removed at the end of it.  It will create the
URL adapter and request object for the WSGI environment provided.

Do not attempt to use this class directly, instead use
:meth:`~flask.Flask.test_request_context` and
:meth:`~flask.Flask.request_context` to create this object.

When the request context is popped, it will evaluate all the
functions registered on the application for teardown execution
(:meth:`~flask.Flask.teardown_request`).

The request context is automatically popped at the end of the request
for you.  In debug mode the request context is kept around if
exceptions happen so that interactive debuggers have a chance to
introspect the data.  With 0.4 this can also be forced for requests
that did not fail and outside of ``DEBUG`` mode.  By setting
``'flask._preserve_context'`` to ``True`` on the WSGI environment the
context will not pop itself at the end of the request.  This is used by
the :meth:`~flask.Flask.test_client` for example to implement the
deferred cleanup functionality.

You might find this helpful for unittests where you need the
information from the context local around for a little longer.  Make
sure to properly :meth:`~werkzeug.LocalStack.pop` the stack yourself in
that situation, otherwise your unittests will leak memory.


- **Bases:** object
- **Methods:** __init__, g, copy, match_request, push, pop, auto_pop, __enter__, __exit__, __repr__

