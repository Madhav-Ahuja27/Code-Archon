# Module: `tests/test_blueprints.py`

**Path:** `C:\temp\flask\tests\test_blueprints.py`
**Lines:** 863
**Avg Complexity:** 3.6


## Description

tests.blueprints
~~~~~~~~~~~~~~~~

Blueprints (and currently modules)

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `functools`

- `pytest`

- `jinja2.TemplateNotFound`

- `werkzeug.http.parse_cache_control_header`

- `flask`

- `flask._compat.text_type`

- `blueprintapp.app`

- `blueprintapp.app`

- `werkzeug.routing.Rule`



## Functions


### `test_blueprint_specific_error_handling(app, client) → None`



- **Line:** 21–56
- **Complexity:** 4
- **Calls:** Blueprint, errorhandler, route, register_blueprint, abort, get


### `frontend_forbidden(e) → None`



- **Line:** 27–28
- **Complexity:** 1
- **Calls:** errorhandler


### `frontend_no() → None`



- **Line:** 31–32
- **Complexity:** 1
- **Calls:** route, abort


### `backend_forbidden(e) → None`



- **Line:** 35–36
- **Complexity:** 1
- **Calls:** errorhandler


### `backend_no() → None`



- **Line:** 39–40
- **Complexity:** 1
- **Calls:** route, abort


### `sideend_no() → None`



- **Line:** 43–44
- **Complexity:** 1
- **Calls:** route, abort


### `app_forbidden(e) → None`



- **Line:** 51–52
- **Complexity:** 1
- **Calls:** errorhandler


### `test_blueprint_specific_user_error_handling(app, client) → None`



- **Line:** 59–90
- **Complexity:** 3
- **Calls:** Blueprint, errorhandler, register_error_handler, route, register_blueprint, isinstance, MyDecoratorException, MyFunctionException, get


### `my_decorator_exception_handler(e) → None`



- **Line:** 69–71
- **Complexity:** 1
- **Calls:** errorhandler, isinstance


### `my_function_exception_handler(e) → None`



- **Line:** 73–75
- **Complexity:** 1
- **Calls:** isinstance


### `blue_deco_test() → None`



- **Line:** 80–81
- **Complexity:** 1
- **Calls:** route, MyDecoratorException


### `blue_func_test() → None`



- **Line:** 84–85
- **Complexity:** 1
- **Calls:** route, MyFunctionException


### `test_blueprint_app_error_handling(app, client) → None`



- **Line:** 93–114
- **Complexity:** 3
- **Calls:** Blueprint, app_errorhandler, route, register_blueprint, abort, get


### `forbidden_handler(e) → None`



- **Line:** 97–98
- **Complexity:** 1
- **Calls:** app_errorhandler


### `app_forbidden() → None`



- **Line:** 101–102
- **Complexity:** 1
- **Calls:** route, abort


### `bp_forbidden() → None`



- **Line:** 107–108
- **Complexity:** 1
- **Calls:** route, abort


### `test_blueprint_prefix_slash(app, client, prefix, rule, url) → None`



- **Line:** 133–141
- **Complexity:** 2
- **Calls:** parametrize, Blueprint, route, register_blueprint, get


### `index() → None`



- **Line:** 137–138
- **Complexity:** 1
- **Calls:** route


### `test_blueprint_url_defaults(app, client) → None`



- **Line:** 144–161
- **Complexity:** 5
- **Calls:** Blueprint, route, register_blueprint, text_type, get


### `foo(bar, baz) → None`



- **Line:** 148–149
- **Complexity:** 1
- **Calls:** route


### `bar(bar) → None`



- **Line:** 152–153
- **Complexity:** 1
- **Calls:** route, text_type


### `test_blueprint_url_processors(app, client) → None`



- **Line:** 164–186
- **Complexity:** 3
- **Calls:** Blueprint, route, register_blueprint, setdefault, pop, url_for, get


### `add_language_code(endpoint, values) → None`



- **Line:** 168–169
- **Complexity:** 1
- **Calls:** setdefault


### `pull_lang_code(endpoint, values) → None`



- **Line:** 172–173
- **Complexity:** 1
- **Calls:** pop


### `index() → None`



- **Line:** 176–177
- **Complexity:** 1
- **Calls:** route, url_for


### `about() → None`



- **Line:** 180–181
- **Complexity:** 1
- **Calls:** route, url_for


### `test_templates_and_static(test_apps) → None`



- **Line:** 189–233
- **Complexity:** 11
- **Calls:** test_client, get, close, strip, parse_cache_control_header, test_request_context, url_for, raises, render_template, Flask


### `test_default_static_cache_timeout(app) → None`



- **Line:** 236–257
- **Complexity:** 3
- **Calls:** MyBlueprint, register_blueprint, test_request_context, send_static_file, parse_cache_control_header, close


### `get_send_file_max_age(self, filename) → None`



- **Line:** 238–239
- **Complexity:** 1
- **Calls:** none


### `test_templates_list(test_apps) → None`



- **Line:** 260–264
- **Complexity:** 2
- **Calls:** sorted, list_templates


### `test_dotted_names(app, client) → None`



- **Line:** 267–288
- **Complexity:** 4
- **Calls:** Blueprint, route, register_blueprint, url_for, strip, get


### `frontend_index() → None`



- **Line:** 272–273
- **Complexity:** 1
- **Calls:** route, url_for


### `frontend_page2() → None`



- **Line:** 276–277
- **Complexity:** 1
- **Calls:** route, url_for


### `backend_index() → None`



- **Line:** 280–281
- **Complexity:** 1
- **Calls:** route, url_for


### `test_dotted_names_from_app(app, client) → None`



- **Line:** 291–305
- **Complexity:** 2
- **Calls:** Blueprint, route, register_blueprint, get, url_for


### `app_index() → None`



- **Line:** 295–296
- **Complexity:** 1
- **Calls:** route, url_for


### `index() → None`



- **Line:** 299–300
- **Complexity:** 1
- **Calls:** route, url_for


### `test_empty_url_defaults(app, client) → None`



- **Line:** 308–319
- **Complexity:** 3
- **Calls:** Blueprint, route, register_blueprint, str, get


### `something(page) → None`



- **Line:** 313–314
- **Complexity:** 1
- **Calls:** route, str


### `test_route_decorator_custom_endpoint(app, client) → None`



- **Line:** 322–351
- **Complexity:** 6
- **Calls:** Blueprint, route, register_blueprint, get


### `foo() → None`



- **Line:** 326–327
- **Complexity:** 1
- **Calls:** route


### `foo_bar() → None`



- **Line:** 330–331
- **Complexity:** 1
- **Calls:** route


### `foo_bar_foo() → None`



- **Line:** 334–335
- **Complexity:** 1
- **Calls:** route


### `bar_foo() → None`



- **Line:** 338–339
- **Complexity:** 1
- **Calls:** route


### `index() → None`



- **Line:** 344–345
- **Complexity:** 1
- **Calls:** route


### `test_route_decorator_custom_endpoint_with_dots(app, client) → None`



- **Line:** 354–412
- **Complexity:** 8
- **Calls:** Blueprint, route, raises, add_url_rule, register_blueprint, get, AssertionError, partial


### `foo() → None`



- **Line:** 358–359
- **Complexity:** 1
- **Calls:** route


### `foo_bar() → None`



- **Line:** 364–365
- **Complexity:** 1
- **Calls:** route


### `foo_bar_foo() → None`



- **Line:** 375–376
- **Complexity:** 1
- **Calls:** route


### `foo_foo_foo() → None`



- **Line:** 383–384
- **Complexity:** 1
- **Calls:** none


### `test_endpoint_decorator(app, client) → None`



- **Line:** 415–429
- **Complexity:** 3
- **Calls:** add, Blueprint, endpoint, register_blueprint, Rule, get


### `foobar() → None`



- **Line:** 423–424
- **Complexity:** 1
- **Calls:** endpoint


### `test_template_filter(app) → None`



- **Line:** 432–442
- **Complexity:** 4
- **Calls:** Blueprint, app_template_filter, register_blueprint, keys


### `my_reverse(s) → None`



- **Line:** 436–437
- **Complexity:** 1
- **Calls:** app_template_filter


### `test_add_template_filter(app) → None`



- **Line:** 445–455
- **Complexity:** 4
- **Calls:** Blueprint, add_app_template_filter, register_blueprint, keys


### `my_reverse(s) → None`



- **Line:** 448–449
- **Complexity:** 1
- **Calls:** none


### `test_template_filter_with_name(app) → None`



- **Line:** 458–468
- **Complexity:** 4
- **Calls:** Blueprint, app_template_filter, register_blueprint, keys


### `my_reverse(s) → None`



- **Line:** 462–463
- **Complexity:** 1
- **Calls:** app_template_filter


### `test_add_template_filter_with_name(app) → None`



- **Line:** 471–481
- **Complexity:** 4
- **Calls:** Blueprint, add_app_template_filter, register_blueprint, keys


### `my_reverse(s) → None`



- **Line:** 474–475
- **Complexity:** 1
- **Calls:** none


### `test_template_filter_with_template(app, client) → None`



- **Line:** 484–498
- **Complexity:** 2
- **Calls:** Blueprint, app_template_filter, register_blueprint, route, get, render_template


### `super_reverse(s) → None`



- **Line:** 488–489
- **Complexity:** 1
- **Calls:** app_template_filter


### `index() → None`



- **Line:** 494–495
- **Complexity:** 1
- **Calls:** route, render_template


### `test_template_filter_after_route_with_template(app, client) → None`



- **Line:** 501–514
- **Complexity:** 2
- **Calls:** route, Blueprint, app_template_filter, register_blueprint, get, render_template


### `index() → None`



- **Line:** 503–504
- **Complexity:** 1
- **Calls:** route, render_template


### `super_reverse(s) → None`



- **Line:** 509–510
- **Complexity:** 1
- **Calls:** app_template_filter


### `test_add_template_filter_with_template(app, client) → None`



- **Line:** 517–531
- **Complexity:** 2
- **Calls:** Blueprint, add_app_template_filter, register_blueprint, route, get, render_template


### `super_reverse(s) → None`



- **Line:** 520–521
- **Complexity:** 1
- **Calls:** none


### `index() → None`



- **Line:** 527–528
- **Complexity:** 1
- **Calls:** route, render_template


### `test_template_filter_with_name_and_template(app, client) → None`



- **Line:** 534–548
- **Complexity:** 2
- **Calls:** Blueprint, app_template_filter, register_blueprint, route, get, render_template


### `my_reverse(s) → None`



- **Line:** 538–539
- **Complexity:** 1
- **Calls:** app_template_filter


### `index() → None`



- **Line:** 544–545
- **Complexity:** 1
- **Calls:** route, render_template


### `test_add_template_filter_with_name_and_template(app, client) → None`



- **Line:** 551–565
- **Complexity:** 2
- **Calls:** Blueprint, add_app_template_filter, register_blueprint, route, get, render_template


### `my_reverse(s) → None`



- **Line:** 554–555
- **Complexity:** 1
- **Calls:** none


### `index() → None`



- **Line:** 561–562
- **Complexity:** 1
- **Calls:** route, render_template


### `test_template_test(app) → None`



- **Line:** 568–578
- **Complexity:** 4
- **Calls:** Blueprint, app_template_test, register_blueprint, isinstance, keys


### `is_boolean(value) → None`



- **Line:** 572–573
- **Complexity:** 1
- **Calls:** app_template_test, isinstance


### `test_add_template_test(app) → None`



- **Line:** 581–591
- **Complexity:** 4
- **Calls:** Blueprint, add_app_template_test, register_blueprint, isinstance, keys


### `is_boolean(value) → None`



- **Line:** 584–585
- **Complexity:** 1
- **Calls:** isinstance


### `test_template_test_with_name(app) → None`



- **Line:** 594–604
- **Complexity:** 4
- **Calls:** Blueprint, app_template_test, register_blueprint, isinstance, keys


### `is_boolean(value) → None`



- **Line:** 598–599
- **Complexity:** 1
- **Calls:** app_template_test, isinstance


### `test_add_template_test_with_name(app) → None`



- **Line:** 607–617
- **Complexity:** 4
- **Calls:** Blueprint, add_app_template_test, register_blueprint, isinstance, keys


### `is_boolean(value) → None`



- **Line:** 610–611
- **Complexity:** 1
- **Calls:** isinstance


### `test_template_test_with_template(app, client) → None`



- **Line:** 620–634
- **Complexity:** 2
- **Calls:** Blueprint, app_template_test, register_blueprint, route, get, isinstance, render_template


### `boolean(value) → None`



- **Line:** 624–625
- **Complexity:** 1
- **Calls:** app_template_test, isinstance


### `index() → None`



- **Line:** 630–631
- **Complexity:** 1
- **Calls:** route, render_template


### `test_template_test_after_route_with_template(app, client) → None`



- **Line:** 637–650
- **Complexity:** 2
- **Calls:** route, Blueprint, app_template_test, register_blueprint, get, render_template, isinstance


### `index() → None`



- **Line:** 639–640
- **Complexity:** 1
- **Calls:** route, render_template


### `boolean(value) → None`



- **Line:** 645–646
- **Complexity:** 1
- **Calls:** app_template_test, isinstance


### `test_add_template_test_with_template(app, client) → None`



- **Line:** 653–667
- **Complexity:** 2
- **Calls:** Blueprint, add_app_template_test, register_blueprint, route, get, isinstance, render_template


### `boolean(value) → None`



- **Line:** 656–657
- **Complexity:** 1
- **Calls:** isinstance


### `index() → None`



- **Line:** 663–664
- **Complexity:** 1
- **Calls:** route, render_template


### `test_template_test_with_name_and_template(app, client) → None`



- **Line:** 670–684
- **Complexity:** 2
- **Calls:** Blueprint, app_template_test, register_blueprint, route, get, isinstance, render_template


### `is_boolean(value) → None`



- **Line:** 674–675
- **Complexity:** 1
- **Calls:** app_template_test, isinstance


### `index() → None`



- **Line:** 680–681
- **Complexity:** 1
- **Calls:** route, render_template


### `test_add_template_test_with_name_and_template(app, client) → None`



- **Line:** 687–701
- **Complexity:** 2
- **Calls:** Blueprint, add_app_template_test, register_blueprint, route, get, isinstance, render_template


### `is_boolean(value) → None`



- **Line:** 690–691
- **Complexity:** 1
- **Calls:** isinstance


### `index() → None`



- **Line:** 697–698
- **Complexity:** 1
- **Calls:** route, render_template


### `test_context_processing(app, client) → None`



- **Line:** 704–741
- **Complexity:** 5
- **Calls:** Blueprint, route, register_blueprint, render_template_string, template_string, get


### `not_answer_context_processor() → None`



- **Line:** 714–715
- **Complexity:** 1
- **Calls:** none


### `answer_context_processor() → None`



- **Line:** 719–720
- **Complexity:** 1
- **Calls:** none


### `bp_page() → None`



- **Line:** 724–725
- **Complexity:** 1
- **Calls:** route, template_string


### `app_page() → None`



- **Line:** 728–729
- **Complexity:** 1
- **Calls:** route, template_string


### `test_template_global(app) → None`



- **Line:** 744–762
- **Complexity:** 6
- **Calls:** Blueprint, app_template_global, register_blueprint, keys, app_context, render_template_string


### `get_answer() → None`



- **Line:** 748–749
- **Complexity:** 1
- **Calls:** app_template_global


### `test_request_processing(app, client) → None`



- **Line:** 765–793
- **Complexity:** 4
- **Calls:** Blueprint, route, register_blueprint, get, append


### `before_bp() → None`



- **Line:** 770–771
- **Complexity:** 1
- **Calls:** append


### `after_bp(response) → None`



- **Line:** 774–777
- **Complexity:** 1
- **Calls:** append


### `teardown_bp(exc) → None`



- **Line:** 780–781
- **Complexity:** 1
- **Calls:** append


### `bp_endpoint() → None`



- **Line:** 785–786
- **Complexity:** 1
- **Calls:** route


### `test_app_request_processing(app, client) → None`



- **Line:** 796–836
- **Complexity:** 6
- **Calls:** Blueprint, register_blueprint, route, append, get


### `before_first_request() → None`



- **Line:** 801–802
- **Complexity:** 1
- **Calls:** append


### `before_app() → None`



- **Line:** 805–806
- **Complexity:** 1
- **Calls:** append


### `after_app(response) → None`



- **Line:** 809–812
- **Complexity:** 1
- **Calls:** append


### `teardown_app(exc) → None`



- **Line:** 815–816
- **Complexity:** 1
- **Calls:** append


### `bp_endpoint() → None`



- **Line:** 822–823
- **Complexity:** 1
- **Calls:** route


### `test_app_url_processors(app, client) → None`



- **Line:** 839–863
- **Complexity:** 3
- **Calls:** Blueprint, route, register_blueprint, setdefault, pop, url_for, get


### `add_language_code(endpoint, values) → None`



- **Line:** 844–845
- **Complexity:** 1
- **Calls:** setdefault


### `pull_lang_code(endpoint, values) → None`



- **Line:** 848–849
- **Complexity:** 1
- **Calls:** pop


### `index() → None`



- **Line:** 853–854
- **Complexity:** 1
- **Calls:** route, url_for


### `about() → None`



- **Line:** 857–858
- **Complexity:** 1
- **Calls:** route, url_for



## Classes


### `MyDecoratorException`



- **Bases:** Exception
- **Methods:** none


### `MyFunctionException`



- **Bases:** Exception
- **Methods:** none


### `MyBlueprint`



- **Bases:** flask.Blueprint
- **Methods:** get_send_file_max_age

