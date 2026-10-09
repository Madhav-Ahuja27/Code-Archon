# Module: `tests/test_views.py`

**Path:** `C:\temp\flask\tests\test_views.py`
**Lines:** 252
**Avg Complexity:** 3.0


## Description

tests.views
~~~~~~~~~~~

Pluggable views.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `pytest`

- `werkzeug.http.parse_set_header`

- `flask.views`



## Functions


### `common_test(app) → None`



- **Line:** 17–24
- **Complexity:** 5
- **Calls:** test_client, parse_set_header, sorted, get, post, put, open


### `test_basic_view(app) → None`



- **Line:** 27–35
- **Complexity:** 1
- **Calls:** add_url_rule, common_test, as_view


### `dispatch_request(self) → None`



- **Line:** 31–32
- **Complexity:** 1
- **Calls:** none


### `test_method_based_view(app) → None`



- **Line:** 38–48
- **Complexity:** 1
- **Calls:** add_url_rule, common_test, as_view


### `get(self) → None`



- **Line:** 40–41
- **Complexity:** 1
- **Calls:** none


### `post(self) → None`



- **Line:** 43–44
- **Complexity:** 1
- **Calls:** none


### `test_view_patching(app) → None`



- **Line:** 51–69
- **Complexity:** 1
- **Calls:** as_view, add_url_rule, common_test


### `get(self) → None`



- **Line:** 53–54
- **Complexity:** 1
- **Calls:** none


### `post(self) → None`



- **Line:** 56–57
- **Complexity:** 1
- **Calls:** none


### `get(self) → None`



- **Line:** 60–61
- **Complexity:** 1
- **Calls:** none


### `post(self) → None`



- **Line:** 63–64
- **Complexity:** 1
- **Calls:** none


### `test_view_inheritance(app, client) → None`



- **Line:** 72–87
- **Complexity:** 2
- **Calls:** add_url_rule, parse_set_header, sorted, as_view, open


### `get(self) → None`



- **Line:** 74–75
- **Complexity:** 1
- **Calls:** none


### `post(self) → None`



- **Line:** 77–78
- **Complexity:** 1
- **Calls:** none


### `delete(self) → None`



- **Line:** 81–82
- **Complexity:** 1
- **Calls:** none


### `test_view_decorators(app, client) → None`



- **Line:** 90–108
- **Complexity:** 3
- **Calls:** add_url_rule, get, make_response, as_view, f


### `add_x_parachute(f) → None`



- **Line:** 91–97
- **Complexity:** 1
- **Calls:** make_response, f


### `new_function() → None`



- **Line:** 92–95
- **Complexity:** 1
- **Calls:** make_response, f


### `dispatch_request(self) → None`



- **Line:** 102–103
- **Complexity:** 1
- **Calls:** none


### `test_view_provide_automatic_options_attr() → None`



- **Line:** 111–148
- **Complexity:** 4
- **Calls:** Flask, add_url_rule, test_client, open, sorted, as_view


### `dispatch_request(self) → None`



- **Line:** 117–118
- **Complexity:** 1
- **Calls:** none


### `dispatch_request(self) → None`



- **Line:** 131–132
- **Complexity:** 1
- **Calls:** none


### `dispatch_request(self) → None`



- **Line:** 142–143
- **Complexity:** 1
- **Calls:** none


### `test_implicit_head(app, client) → None`



- **Line:** 151–162
- **Complexity:** 5
- **Calls:** add_url_rule, get, head, Response, as_view


### `get(self) → None`



- **Line:** 153–154
- **Complexity:** 1
- **Calls:** Response


### `test_explicit_head(app, client) → None`



- **Line:** 165–178
- **Complexity:** 4
- **Calls:** add_url_rule, get, head, Response, as_view


### `get(self) → None`



- **Line:** 167–168
- **Complexity:** 1
- **Calls:** none


### `head(self) → None`



- **Line:** 170–171
- **Complexity:** 1
- **Calls:** Response


### `test_endpoint_override(app) → None`



- **Line:** 181–196
- **Complexity:** 1
- **Calls:** add_url_rule, common_test, raises, as_view


### `dispatch_request(self) → None`



- **Line:** 187–188
- **Complexity:** 1
- **Calls:** none


### `test_methods_var_inheritance(app, client) → None`



- **Line:** 199–214
- **Complexity:** 4
- **Calls:** add_url_rule, as_view, get, open


### `get(self) → None`



- **Line:** 204–205
- **Complexity:** 1
- **Calls:** none


### `propfind(self) → None`



- **Line:** 207–208
- **Complexity:** 1
- **Calls:** none


### `test_multiple_inheritance(app, client) → None`



- **Line:** 217–233
- **Complexity:** 4
- **Calls:** add_url_rule, sorted, as_view, get, delete


### `get(self) → None`



- **Line:** 219–220
- **Complexity:** 1
- **Calls:** none


### `delete(self) → None`



- **Line:** 223–224
- **Complexity:** 1
- **Calls:** none


### `test_remove_method_from_parent(app, client) → None`



- **Line:** 236–252
- **Complexity:** 4
- **Calls:** add_url_rule, sorted, as_view, get, post


### `get(self) → None`



- **Line:** 238–239
- **Complexity:** 1
- **Calls:** none


### `post(self) → None`



- **Line:** 242–243
- **Complexity:** 1
- **Calls:** none



## Classes


### `Index`



- **Bases:** flask.views.View
- **Methods:** dispatch_request


### `Index`



- **Bases:** flask.views.MethodView
- **Methods:** get, post


### `Index`



- **Bases:** flask.views.MethodView
- **Methods:** get, post


### `Other`



- **Bases:** Index
- **Methods:** get, post


### `Index`



- **Bases:** flask.views.MethodView
- **Methods:** get, post


### `BetterIndex`



- **Bases:** Index
- **Methods:** delete


### `Index`



- **Bases:** flask.views.View
- **Methods:** dispatch_request


### `Index1`



- **Bases:** flask.views.View
- **Methods:** dispatch_request


### `Index2`



- **Bases:** flask.views.View
- **Methods:** dispatch_request


### `Index3`



- **Bases:** flask.views.View
- **Methods:** dispatch_request


### `Index`



- **Bases:** flask.views.MethodView
- **Methods:** get


### `Index`



- **Bases:** flask.views.MethodView
- **Methods:** get, head


### `Index`



- **Bases:** flask.views.View
- **Methods:** dispatch_request


### `BaseView`



- **Bases:** flask.views.MethodView
- **Methods:** none


### `ChildView`



- **Bases:** BaseView
- **Methods:** get, propfind


### `GetView`



- **Bases:** flask.views.MethodView
- **Methods:** get


### `DeleteView`



- **Bases:** flask.views.MethodView
- **Methods:** delete


### `GetDeleteView`



- **Bases:** GetView, DeleteView
- **Methods:** none


### `GetView`



- **Bases:** flask.views.MethodView
- **Methods:** get


### `OtherView`



- **Bases:** flask.views.MethodView
- **Methods:** post


### `View`



- **Bases:** GetView, OtherView
- **Methods:** none

