# Module: `src/flask/sessions.py`

**Path:** `C:\temp\flask\src\flask\sessions.py`
**Lines:** 388
**Avg Complexity:** 2.2


## Description

flask.sessions
~~~~~~~~~~~~~~

Implements cookie based sessions based on itsdangerous.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `hashlib`

- `warnings`

- `datetime.datetime`

- `itsdangerous.BadSignature`

- `itsdangerous.URLSafeTimedSerializer`

- `werkzeug.datastructures.CallbackDict`

- `_compat.collections_abc`

- `helpers.is_ip`

- `helpers.total_seconds`

- `json.tag.TaggedJSONSerializer`



## Functions


### `permanent(self) → None`


This reflects the ``'_permanent'`` key in the dict.


- **Line:** 29–31
- **Complexity:** 1
- **Calls:** get


### `permanent(self, value) → None`



- **Line:** 34–35
- **Complexity:** 1
- **Calls:** bool


### `__init__(self, initial) → None`



- **Line:** 75–80
- **Complexity:** 1
- **Calls:** __init__, super


### `on_update(self) → None`



- **Line:** 76–78
- **Complexity:** 1
- **Calls:** none


### `__getitem__(self, key) → None`



- **Line:** 82–84
- **Complexity:** 1
- **Calls:** __getitem__, super


### `get(self, key, default) → None`



- **Line:** 86–88
- **Complexity:** 1
- **Calls:** get, super


### `setdefault(self, key, default) → None`



- **Line:** 90–92
- **Complexity:** 1
- **Calls:** setdefault, super


### `_fail(self) → None`



- **Line:** 101–106
- **Complexity:** 1
- **Calls:** RuntimeError


### `make_null_session(self, app) → None`


Creates a null session which acts as a replacement object if the
real session support could not be loaded due to a configuration
error.  This mainly aids the user experience because the job of the
null session is to still support lookup without complaining but
modifications are answered with a helpful error message of what
failed.

This creates an instance of :attr:`null_session_class` by default.


- **Line:** 155–165
- **Complexity:** 1
- **Calls:** null_session_class


### `is_null_session(self, obj) → None`


Checks if a given object is a null session.  Null sessions are
not asked to be saved.

This checks if the object is an instance of :attr:`null_session_class`
by default.


- **Line:** 167–174
- **Complexity:** 1
- **Calls:** isinstance


### `get_cookie_domain(self, app) → None`


Returns the domain that should be set for the session cookie.

Uses ``SESSION_COOKIE_DOMAIN`` if it is configured, otherwise
falls back to detecting the domain based on ``SERVER_NAME``.

Once detected (or if not set at all), ``SESSION_COOKIE_DOMAIN`` is
updated to avoid re-running the logic.


- **Line:** 176–232
- **Complexity:** 8
- **Calls:** lstrip, is_ip, warn, format, get_cookie_path, rsplit


### `get_cookie_path(self, app) → None`


Returns the path for which the cookie should be valid.  The
default implementation uses the value from the ``SESSION_COOKIE_PATH``
config var if it's set, and falls back to ``APPLICATION_ROOT`` or
uses ``/`` if it's ``None``.


- **Line:** 234–240
- **Complexity:** 2
- **Calls:** none


### `get_cookie_httponly(self, app) → None`


Returns True if the session cookie should be httponly.  This
currently just returns the value of the ``SESSION_COOKIE_HTTPONLY``
config var.


- **Line:** 242–247
- **Complexity:** 1
- **Calls:** none


### `get_cookie_secure(self, app) → None`


Returns True if the cookie should be secure.  This currently
just returns the value of the ``SESSION_COOKIE_SECURE`` setting.


- **Line:** 249–253
- **Complexity:** 1
- **Calls:** none


### `get_cookie_samesite(self, app) → None`


Return ``'Strict'`` or ``'Lax'`` if the cookie should use the
``SameSite`` attribute. This currently just returns the value of
the :data:`SESSION_COOKIE_SAMESITE` setting.


- **Line:** 255–260
- **Complexity:** 1
- **Calls:** none


### `get_expiration_time(self, app, session) → None`


A helper method that returns an expiration date for the session
or ``None`` if the session is linked to the browser session.  The
default implementation returns now + the permanent session
lifetime configured on the application.


- **Line:** 262–269
- **Complexity:** 2
- **Calls:** utcnow


### `should_set_cookie(self, app, session) → None`


Used by session backends to determine if a ``Set-Cookie`` header
should be set for this session cookie for this response. If the session
has been modified, the cookie is set. If the session is permanent and
the ``SESSION_REFRESH_EACH_REQUEST`` config is true, the cookie is
always set.

This check is usually skipped if the session was deleted.

.. versionadded:: 0.11


- **Line:** 271–285
- **Complexity:** 3
- **Calls:** none


### `open_session(self, app, request) → None`


This method has to be implemented and must either return ``None``
in case the loading failed because of a configuration error or an
instance of a session object which implements a dictionary like
interface + the methods and attributes on :class:`SessionMixin`.


- **Line:** 287–293
- **Complexity:** 4
- **Calls:** NotImplementedError


### `save_session(self, app, session, response) → None`


This is called for actual sessions returned by :meth:`open_session`
at the end of the request.  This is still called during a request
context so if you absolutely need access to the request you can do
that.


- **Line:** 295–301
- **Complexity:** 5
- **Calls:** NotImplementedError


### `get_signing_serializer(self, app) → None`



- **Line:** 326–337
- **Complexity:** 2
- **Calls:** dict, URLSafeTimedSerializer


### `open_session(self, app, request) → None`



- **Line:** 339–351
- **Complexity:** 4
- **Calls:** get_signing_serializer, get, total_seconds, session_class, loads


### `save_session(self, app, session, response) → None`



- **Line:** 353–388
- **Complexity:** 5
- **Calls:** get_cookie_domain, get_cookie_path, get_cookie_httponly, get_cookie_secure, get_cookie_samesite, get_expiration_time, dumps, set_cookie, add, should_set_cookie, dict, delete_cookie, get_signing_serializer



## Classes


### `SessionMixin`


Expands a basic dictionary with session attributes.


- **Bases:** collections_abc.MutableMapping
- **Methods:** permanent


### `SecureCookieSession`


Base class for sessions based on signed cookies.

This session backend will set the :attr:`modified` and
:attr:`accessed` attributes. It cannot reliably track whether a
session is new (vs. empty), so :attr:`new` remains hard coded to
``False``.


- **Bases:** CallbackDict, SessionMixin
- **Methods:** __init__, __getitem__, get, setdefault


### `NullSession`


Class used to generate nicer error messages if sessions are not
available.  Will still allow read-only access to the empty session
but fail on setting.


- **Bases:** SecureCookieSession
- **Methods:** _fail


### `SessionInterface`


The basic interface you have to implement in order to replace the
default session interface which uses werkzeug's securecookie
implementation.  The only methods you have to implement are
:meth:`open_session` and :meth:`save_session`, the others have
useful defaults which you don't need to change.

The session object returned by the :meth:`open_session` method has to
provide a dictionary like interface plus the properties and methods
from the :class:`SessionMixin`.  We recommend just subclassing a dict
and adding that mixin::

    class Session(dict, SessionMixin):
        pass

If :meth:`open_session` returns ``None`` Flask will call into
:meth:`make_null_session` to create a session that acts as replacement
if the session support cannot work because some requirement is not
fulfilled.  The default :class:`NullSession` class that is created
will complain that the secret key was not set.

To replace the session interface on an application all you have to do
is to assign :attr:`flask.Flask.session_interface`::

    app = Flask(__name__)
    app.session_interface = MySessionInterface()

.. versionadded:: 0.8


- **Bases:** object
- **Methods:** make_null_session, is_null_session, get_cookie_domain, get_cookie_path, get_cookie_httponly, get_cookie_secure, get_cookie_samesite, get_expiration_time, should_set_cookie, open_session, save_session


### `SecureCookieSessionInterface`


The default session interface that stores sessions in signed cookies
through the :mod:`itsdangerous` module.


- **Bases:** SessionInterface
- **Methods:** get_signing_serializer, open_session, save_session

