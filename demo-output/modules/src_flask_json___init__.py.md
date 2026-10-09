# Module: `src/flask/json/__init__.py`

**Path:** `C:\temp\flask\src\flask\json\__init__.py`
**Lines:** 376
**Avg Complexity:** 4.2


## Description

flask.json
~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `codecs`

- `io`

- `uuid`

- `datetime.date`

- `datetime.datetime`

- `itsdangerous.json`

- `jinja2.Markup`

- `werkzeug.http.http_date`

- `_compat.PY2`

- `_compat.text_type`

- `globals.current_app`

- `globals.request`

- `dataclasses`



## Functions


### `_wrap_reader_for_text(fp, encoding) → None`



- **Line:** 47–50
- **Complexity:** 2
- **Calls:** isinstance, read, TextIOWrapper, BufferedReader


### `_wrap_writer_for_text(fp, encoding) → None`



- **Line:** 53–58
- **Complexity:** 2
- **Calls:** write, TextIOWrapper


### `default(self, o) → None`


Implement this method in a subclass such that it returns a
serializable object for ``o``, or calls the base implementation (to
raise a :exc:`TypeError`).

For example, to support arbitrary iterators, you could implement
default like this::

    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, o)


- **Line:** 73–100
- **Complexity:** 7
- **Calls:** isinstance, hasattr, default, http_date, str, is_dataclass, asdict, text_type, utctimetuple, timetuple, __html__


### `_dump_arg_defaults(kwargs, app) → None`


Inject default arguments for dump functions.


- **Line:** 111–128
- **Complexity:** 7
- **Calls:** setdefault, get


### `_load_arg_defaults(kwargs, app) → None`


Inject default arguments for load functions.


- **Line:** 131–142
- **Complexity:** 6
- **Calls:** setdefault, get


### `detect_encoding(data) → None`


Detect which UTF codec was used to encode the given bytes.

The latest JSON standard (:rfc:`8259`) suggests that only UTF-8 is
accepted. Older documents allowed 8, 16, or 32. 16 and 32 can be big
or little endian. Some editors or libraries may prepend a BOM.

:param data: Bytes in unknown UTF encoding.
:return: UTF encoding name


- **Line:** 145–185
- **Complexity:** 12
- **Calls:** len, startswith


### `dumps(obj, app) → None`


Serialize ``obj`` to a JSON-formatted string. If there is an
app context pushed, use the current app's configured encoder
(:attr:`~flask.Flask.json_encoder`), or fall back to the default
:class:`JSONEncoder`.

Takes the same arguments as the built-in :func:`json.dumps`, and
does some extra configuration based on the application. If the
simplejson package is installed, it is preferred.

:param obj: Object to serialize to JSON.
:param app: App instance to use to configure the JSON encoder.
    Uses ``current_app`` if not given, and falls back to the default
    encoder when not in an app context.
:param kwargs: Extra arguments passed to :func:`json.dumps`.

.. versionchanged:: 1.0.3

    ``app`` can be passed directly, rather than requiring an app
    context for configuration.


- **Line:** 188–214
- **Complexity:** 3
- **Calls:** _dump_arg_defaults, pop, dumps, isinstance, encode


### `dump(obj, fp, app) → None`


Like :func:`dumps` but writes into a file object.


- **Line:** 217–223
- **Complexity:** 2
- **Calls:** _dump_arg_defaults, pop, dump, _wrap_writer_for_text


### `loads(s, app) → None`


Deserialize an object from a JSON-formatted string ``s``. If
there is an app context pushed, use the current app's configured
decoder (:attr:`~flask.Flask.json_decoder`), or fall back to the
default :class:`JSONDecoder`.

Takes the same arguments as the built-in :func:`json.loads`, and
does some extra configuration based on the application. If the
simplejson package is installed, it is preferred.

:param s: JSON string to deserialize.
:param app: App instance to use to configure the JSON decoder.
    Uses ``current_app`` if not given, and falls back to the default
    encoder when not in an app context.
:param kwargs: Extra arguments passed to :func:`json.loads`.

.. versionchanged:: 1.0.3

    ``app`` can be passed directly, rather than requiring an app
    context for configuration.


- **Line:** 226–253
- **Complexity:** 3
- **Calls:** _load_arg_defaults, isinstance, loads, pop, decode, detect_encoding


### `load(fp, app) → None`


Like :func:`loads` but reads from a file object.


- **Line:** 256–261
- **Complexity:** 3
- **Calls:** _load_arg_defaults, load, _wrap_reader_for_text, pop


### `htmlsafe_dumps(obj) → None`


Works exactly like :func:`dumps` but is safe for use in ``<script>``
tags.  It accepts the same arguments and returns a JSON string.  Note that
this is available in templates through the ``|tojson`` filter which will
also mark the result as safe.  Due to how this function escapes certain
characters this is safe even if used outside of ``<script>`` tags.

The following characters are escaped in strings:

-   ``<``
-   ``>``
-   ``&``
-   ``'``

This makes it safe to embed such strings in any place in HTML with the
notable exception of double quoted attributes.  In that case single
quote your attributes or HTML escape it in addition.

.. versionchanged:: 0.10
   This function's return value is now always safe for HTML usage, even
   if outside of script tags or if used in XHTML.  This rule does not
   hold true when using this function in HTML attributes that are double
   quoted.  Always single quote attributes if you use the ``|tojson``
   filter.  Alternatively use ``|tojson|forceescape``.


- **Line:** 264–298
- **Complexity:** 2
- **Calls:** replace, dumps


### `htmlsafe_dump(obj, fp) → None`


Like :func:`htmlsafe_dumps` but writes into a file object.


- **Line:** 301–303
- **Complexity:** 1
- **Calls:** write, text_type, htmlsafe_dumps


### `jsonify() → None`


This function wraps :func:`dumps` to add a few enhancements that make
life easier.  It turns the JSON output into a :class:`~flask.Response`
object with the :mimetype:`application/json` mimetype.  For convenience, it
also converts multiple arguments into an array or multiple keyword arguments
into a dict.  This means that both ``jsonify(1,2,3)`` and
``jsonify([1,2,3])`` serialize to ``[1,2,3]``.

For clarity, the JSON serialization behavior has the following differences
from :func:`dumps`:

1. Single argument: Passed straight through to :func:`dumps`.
2. Multiple arguments: Converted to an array before being passed to
   :func:`dumps`.
3. Multiple keyword arguments: Converted to a dict before being passed to
   :func:`dumps`.
4. Both args and kwargs: Behavior undefined and will throw an exception.

Example usage::

    from flask import jsonify

    @app.route('/_get_current_user')
    def get_current_user():
        return jsonify(username=g.user.username,
                       email=g.user.email,
                       id=g.user.id)

This will send a JSON response like this to the browser::

    {
        "username": "admin",
        "email": "admin@localhost",
        "id": 42
    }


.. versionchanged:: 0.11
   Added support for serializing top-level arrays. This introduces a
   security risk in ancient browsers. See :ref:`json-security` for details.

This function's response will be pretty printed if the
``JSONIFY_PRETTYPRINT_REGULAR`` config parameter is set to True or the
Flask app is running in debug mode. Compressed (not pretty) formatting
currently means no indents and no spaces after separators.

.. versionadded:: 0.2


- **Line:** 306–372
- **Complexity:** 7
- **Calls:** response_class, TypeError, len, dumps


### `tojson_filter(obj) → None`



- **Line:** 375–376
- **Complexity:** 1
- **Calls:** Markup, htmlsafe_dumps



## Classes


### `JSONEncoder`


The default Flask JSON encoder. This one extends the default
encoder by also supporting ``datetime``, ``UUID``, ``dataclasses``,
and ``Markup`` objects.

``datetime`` objects are serialized as RFC 822 datetime strings.
This is the same as the HTTP date format.

In order to support more data types, override the :meth:`default`
method.


- **Bases:** _json.JSONEncoder
- **Methods:** default


### `JSONDecoder`


The default JSON decoder.  This one does not change the behavior from
the default simplejson decoder.  Consult the :mod:`json` documentation
for more information.  This decoder is not only used for the load
functions of this module but also :attr:`~flask.Request`.


- **Bases:** _json.JSONDecoder
- **Methods:** none

