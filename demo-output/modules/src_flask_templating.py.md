# Module: `src/flask/templating.py`

**Path:** `C:\temp\flask\src\flask\templating.py`
**Lines:** 155
**Avg Complexity:** 2.8


## Description

flask.templating
~~~~~~~~~~~~~~~~

Implements the bridge to Jinja2.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `jinja2.BaseLoader`

- `jinja2.Environment`

- `jinja2.TemplateNotFound`

- `globals._app_ctx_stack`

- `globals._request_ctx_stack`

- `signals.before_render_template`

- `signals.template_rendered`

- `debughelpers.explain_template_loading_attempts`



## Functions


### `_default_template_ctx_processor() → None`


Default template context processor.  Injects `request`,
`session` and `g`.


- **Line:** 21–33
- **Complexity:** 3
- **Calls:** none


### `__init__(self, app) → None`



- **Line:** 42–46
- **Complexity:** 1
- **Calls:** __init__, create_global_jinja_loader


### `__init__(self, app) → None`



- **Line:** 54–55
- **Complexity:** 1
- **Calls:** none


### `get_source(self, environment, template) → None`



- **Line:** 57–60
- **Complexity:** 2
- **Calls:** _get_source_fast, _get_source_explained


### `_get_source_explained(self, environment, template) → None`



- **Line:** 62–81
- **Complexity:** 5
- **Calls:** _iter_loaders, explain_template_loading_attempts, TemplateNotFound, append, get_source


### `_get_source_fast(self, environment, template) → None`



- **Line:** 83–89
- **Complexity:** 3
- **Calls:** _iter_loaders, TemplateNotFound, get_source


### `_iter_loaders(self, template) → None`



- **Line:** 91–99
- **Complexity:** 4
- **Calls:** iter_blueprints


### `list_templates(self) → None`



- **Line:** 101–113
- **Complexity:** 5
- **Calls:** set, iter_blueprints, list, update, list_templates, add


### `_render(template, context, app) → None`


Renders the template and fires the signal


- **Line:** 116–122
- **Complexity:** 1
- **Calls:** send, render


### `render_template(template_name_or_list) → None`


Renders a template from the template folder with the given
context.

:param template_name_or_list: the name of the template to be
                              rendered, or an iterable with template names
                              the first one existing will be rendered
:param context: the variables that should be available in the
                context of the template.


- **Line:** 125–141
- **Complexity:** 1
- **Calls:** update_template_context, _render, get_or_select_template


### `render_template_string(source) → None`


Renders a template from the given template source string
with the given context. Template variables will be autoescaped.

:param source: the source code of the template to be
               rendered
:param context: the variables that should be available in the
                context of the template.


- **Line:** 144–155
- **Complexity:** 1
- **Calls:** update_template_context, _render, from_string



## Classes


### `Environment`


Works like a regular Jinja2 environment but has some additional
knowledge of how Flask's blueprint works so that it can prepend the
name of the blueprint to referenced templates if necessary.


- **Bases:** BaseEnvironment
- **Methods:** __init__


### `DispatchingJinjaLoader`


A loader that looks for templates in the application and all
the blueprint folders.


- **Bases:** BaseLoader
- **Methods:** __init__, get_source, _get_source_explained, _get_source_fast, _iter_loaders, list_templates

