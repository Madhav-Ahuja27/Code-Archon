# Module: `tests/test_templating.py`

**Path:** `C:\temp\flask\tests\test_templating.py`
**Lines:** 453
**Avg Complexity:** 3.1


## Description

tests.templating
~~~~~~~~~~~~~~~~

Template functionality

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `logging`

- `pytest`

- `werkzeug.serving`

- `jinja2.TemplateNotFound`

- `flask`

- `blueprintapp.app`

- `jinja2.DictLoader`



## Functions


### `test_context_processing(app, client) → None`



- **Line:** 20–30
- **Complexity:** 2
- **Calls:** route, get, render_template


### `context_processor() → None`



- **Line:** 22–23
- **Complexity:** 1
- **Calls:** none


### `index() → None`



- **Line:** 26–27
- **Complexity:** 1
- **Calls:** route, render_template


### `test_original_win(app, client) → None`



- **Line:** 33–39
- **Complexity:** 2
- **Calls:** route, get, render_template_string


### `index() → None`



- **Line:** 35–36
- **Complexity:** 1
- **Calls:** route, render_template_string


### `test_request_less_rendering(app, app_ctx) → None`



- **Line:** 42–50
- **Complexity:** 2
- **Calls:** render_template_string, dict


### `context_processor() → None`



- **Line:** 46–47
- **Complexity:** 1
- **Calls:** dict


### `test_standard_context(app, client) → None`



- **Line:** 53–68
- **Complexity:** 2
- **Calls:** route, get, render_template_string, split


### `index() → None`



- **Line:** 55–65
- **Complexity:** 1
- **Calls:** route, render_template_string


### `test_escaping(app, client) → None`



- **Line:** 71–88
- **Complexity:** 2
- **Calls:** route, splitlines, render_template, Markup, get


### `index() → None`



- **Line:** 75–78
- **Complexity:** 1
- **Calls:** route, render_template, Markup


### `test_no_escaping(app, client) → None`



- **Line:** 91–110
- **Complexity:** 2
- **Calls:** route, splitlines, render_template, Markup, get


### `index() → None`



- **Line:** 95–98
- **Complexity:** 1
- **Calls:** route, render_template, Markup


### `test_escaping_without_template_filename(app, client, req_ctx) → None`



- **Line:** 113–115
- **Complexity:** 3
- **Calls:** render_template_string, render_template


### `test_macros(app, req_ctx) → None`



- **Line:** 118–120
- **Complexity:** 2
- **Calls:** get_template_attribute, macro


### `test_template_filter(app) → None`



- **Line:** 123–130
- **Complexity:** 4
- **Calls:** template_filter, keys


### `my_reverse(s) → None`



- **Line:** 125–126
- **Complexity:** 1
- **Calls:** template_filter


### `test_add_template_filter(app) → None`



- **Line:** 133–140
- **Complexity:** 4
- **Calls:** add_template_filter, keys


### `my_reverse(s) → None`



- **Line:** 134–135
- **Complexity:** 1
- **Calls:** none


### `test_template_filter_with_name(app) → None`



- **Line:** 143–150
- **Complexity:** 4
- **Calls:** template_filter, keys


### `my_reverse(s) → None`



- **Line:** 145–146
- **Complexity:** 1
- **Calls:** template_filter


### `test_add_template_filter_with_name(app) → None`



- **Line:** 153–160
- **Complexity:** 4
- **Calls:** add_template_filter, keys


### `my_reverse(s) → None`



- **Line:** 154–155
- **Complexity:** 1
- **Calls:** none


### `test_template_filter_with_template(app, client) → None`



- **Line:** 163–173
- **Complexity:** 2
- **Calls:** template_filter, route, get, render_template


### `super_reverse(s) → None`



- **Line:** 165–166
- **Complexity:** 1
- **Calls:** template_filter


### `index() → None`



- **Line:** 169–170
- **Complexity:** 1
- **Calls:** route, render_template


### `test_add_template_filter_with_template(app, client) → None`



- **Line:** 176–187
- **Complexity:** 2
- **Calls:** add_template_filter, route, get, render_template


### `super_reverse(s) → None`



- **Line:** 177–178
- **Complexity:** 1
- **Calls:** none


### `index() → None`



- **Line:** 183–184
- **Complexity:** 1
- **Calls:** route, render_template


### `test_template_filter_with_name_and_template(app, client) → None`



- **Line:** 190–200
- **Complexity:** 2
- **Calls:** template_filter, route, get, render_template


### `my_reverse(s) → None`



- **Line:** 192–193
- **Complexity:** 1
- **Calls:** template_filter


### `index() → None`



- **Line:** 196–197
- **Complexity:** 1
- **Calls:** route, render_template


### `test_add_template_filter_with_name_and_template(app, client) → None`



- **Line:** 203–214
- **Complexity:** 2
- **Calls:** add_template_filter, route, get, render_template


### `my_reverse(s) → None`



- **Line:** 204–205
- **Complexity:** 1
- **Calls:** none


### `index() → None`



- **Line:** 210–211
- **Complexity:** 1
- **Calls:** route, render_template


### `test_template_test(app) → None`



- **Line:** 217–224
- **Complexity:** 4
- **Calls:** template_test, isinstance, keys


### `boolean(value) → None`



- **Line:** 219–220
- **Complexity:** 1
- **Calls:** template_test, isinstance


### `test_add_template_test(app) → None`



- **Line:** 227–234
- **Complexity:** 4
- **Calls:** add_template_test, isinstance, keys


### `boolean(value) → None`



- **Line:** 228–229
- **Complexity:** 1
- **Calls:** isinstance


### `test_template_test_with_name(app) → None`



- **Line:** 237–244
- **Complexity:** 4
- **Calls:** template_test, isinstance, keys


### `is_boolean(value) → None`



- **Line:** 239–240
- **Complexity:** 1
- **Calls:** template_test, isinstance


### `test_add_template_test_with_name(app) → None`



- **Line:** 247–254
- **Complexity:** 4
- **Calls:** add_template_test, isinstance, keys


### `is_boolean(value) → None`



- **Line:** 248–249
- **Complexity:** 1
- **Calls:** isinstance


### `test_template_test_with_template(app, client) → None`



- **Line:** 257–267
- **Complexity:** 2
- **Calls:** template_test, route, get, isinstance, render_template


### `boolean(value) → None`



- **Line:** 259–260
- **Complexity:** 1
- **Calls:** template_test, isinstance


### `index() → None`



- **Line:** 263–264
- **Complexity:** 1
- **Calls:** route, render_template


### `test_add_template_test_with_template(app, client) → None`



- **Line:** 270–281
- **Complexity:** 2
- **Calls:** add_template_test, route, get, isinstance, render_template


### `boolean(value) → None`



- **Line:** 271–272
- **Complexity:** 1
- **Calls:** isinstance


### `index() → None`



- **Line:** 277–278
- **Complexity:** 1
- **Calls:** route, render_template


### `test_template_test_with_name_and_template(app, client) → None`



- **Line:** 284–294
- **Complexity:** 2
- **Calls:** template_test, route, get, isinstance, render_template


### `is_boolean(value) → None`



- **Line:** 286–287
- **Complexity:** 1
- **Calls:** template_test, isinstance


### `index() → None`



- **Line:** 290–291
- **Complexity:** 1
- **Calls:** route, render_template


### `test_add_template_test_with_name_and_template(app, client) → None`



- **Line:** 297–308
- **Complexity:** 2
- **Calls:** add_template_test, route, get, isinstance, render_template


### `is_boolean(value) → None`



- **Line:** 298–299
- **Complexity:** 1
- **Calls:** isinstance


### `index() → None`



- **Line:** 304–305
- **Complexity:** 1
- **Calls:** route, render_template


### `test_add_template_global(app, app_ctx) → None`



- **Line:** 311–321
- **Complexity:** 5
- **Calls:** template_global, render_template_string, keys


### `get_stuff() → None`



- **Line:** 313–314
- **Complexity:** 1
- **Calls:** template_global


### `test_custom_template_loader(client) → None`



- **Line:** 324–339
- **Complexity:** 2
- **Calls:** MyFlask, route, test_client, get, render_template, DictLoader


### `create_global_jinja_loader(self) → None`



- **Line:** 326–329
- **Complexity:** 1
- **Calls:** DictLoader


### `index() → None`



- **Line:** 334–335
- **Complexity:** 1
- **Calls:** route, render_template


### `test_iterable_loader(app, client) → None`



- **Line:** 342–359
- **Complexity:** 2
- **Calls:** route, get, render_template


### `context_processor() → None`



- **Line:** 344–345
- **Complexity:** 1
- **Calls:** none


### `index() → None`



- **Line:** 348–356
- **Complexity:** 1
- **Calls:** route, render_template


### `test_templates_auto_reload(app) → None`



- **Line:** 362–391
- **Complexity:** 12
- **Calls:** Flask


### `test_templates_auto_reload_debug_run(app, monkeypatch) → None`



- **Line:** 394–406
- **Complexity:** 5
- **Calls:** setattr, run


### `run_simple_mock() → None`



- **Line:** 395–396
- **Complexity:** 1
- **Calls:** none


### `test_template_loader_debugging(test_apps, monkeypatch) → None`



- **Line:** 409–442
- **Complexity:** 3
- **Calls:** test_client, setitem, setattr, len, append, str, getLogger, raises, get, _TestHandler


### `handle(self, record) → None`



- **Line:** 415–429
- **Complexity:** 1
- **Calls:** append, str


### `test_custom_jinja_env() → None`



- **Line:** 445–453
- **Complexity:** 2
- **Calls:** CustomFlask, isinstance



## Classes


### `MyFlask`



- **Bases:** flask.Flask
- **Methods:** create_global_jinja_loader


### `_TestHandler`



- **Bases:** logging.Handler
- **Methods:** handle


### `CustomEnvironment`



- **Bases:** flask.templating.Environment
- **Methods:** none


### `CustomFlask`



- **Bases:** flask.Flask
- **Methods:** none

