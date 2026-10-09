# Module: `src/flask/wrappers.py`

**Path:** `C:\temp\flask\src\flask\wrappers.py`
**Lines:** 137
**Avg Complexity:** 2.9


## Description

flask.wrappers
~~~~~~~~~~~~~~

Implements the WSGI wrappers (request and response).

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `werkzeug.exceptions.BadRequest`

- `werkzeug.wrappers.Request`

- `werkzeug.wrappers.Response`

- `werkzeug.wrappers.json.JSONMixin`

- `json`

- `globals.current_app`

- `debughelpers.attach_enctype_error_multidict`



## Functions


### `on_json_loading_failed(self, e) → None`



- **Line:** 23–27
- **Complexity:** 3
- **Calls:** BadRequest, format


### `max_content_length(self) → None`


Read-only view of the ``MAX_CONTENT_LENGTH`` config key.


- **Line:** 66–69
- **Complexity:** 2
- **Calls:** none


### `endpoint(self) → None`


The endpoint that matched the request.  This in combination with
:attr:`view_args` can be used to reconstruct the same or a
modified URL.  If an exception happened when matching, this will
be ``None``.


- **Line:** 72–79
- **Complexity:** 2
- **Calls:** none


### `blueprint(self) → None`


The name of the current blueprint


- **Line:** 82–85
- **Complexity:** 3
- **Calls:** rsplit


### `_load_form_data(self) → None`



- **Line:** 87–100
- **Complexity:** 5
- **Calls:** _load_form_data, attach_enctype_error_multidict


### `_get_data_for_json(self, cache) → None`



- **Line:** 123–124
- **Complexity:** 1
- **Calls:** get_data


### `max_cookie_size(self) → None`


Read-only view of the :data:`MAX_COOKIE_SIZE` config key.

See :attr:`~werkzeug.wrappers.BaseResponse.max_cookie_size` in
Werkzeug's docs.


- **Line:** 127–137
- **Complexity:** 2
- **Calls:** super



## Classes


### `JSONMixin`



- **Bases:** _JSONMixin
- **Methods:** on_json_loading_failed


### `Request`


The request object used by default in Flask.  Remembers the
matched endpoint and view arguments.

It is what ends up as :class:`~flask.request`.  If you want to replace
the request object used you can subclass this and set
:attr:`~flask.Flask.request_class` to your subclass.

The request object is a :class:`~werkzeug.wrappers.Request` subclass and
provides all of the attributes Werkzeug defines plus a few Flask
specific ones.


- **Bases:** RequestBase, JSONMixin
- **Methods:** max_content_length, endpoint, blueprint, _load_form_data


### `Response`


The response object that is used by default in Flask.  Works like the
response object from Werkzeug but is set to have an HTML mimetype by
default.  Quite often you don't have to create this object yourself because
:meth:`~flask.Flask.make_response` will take care of that for you.

If you want to replace the response object used you can subclass this and
set :attr:`~flask.Flask.response_class` to your subclass.

.. versionchanged:: 1.0
    JSON support is added to the response, like the request. This is useful
    when testing to get the test client response data as JSON.

.. versionchanged:: 1.0

    Added :attr:`max_cookie_size`.


- **Bases:** ResponseBase, JSONMixin
- **Methods:** _get_data_for_json, max_cookie_size

