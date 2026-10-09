# Module: `tests/test_cli.py`

**Path:** `C:\temp\flask\tests\test_cli.py`
**Lines:** 667
**Avg Complexity:** 3.4


## Description

tests.test_cli
~~~~~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `__future__.absolute_import`

- `os`

- `ssl`

- `sys`

- `types`

- `functools.partial`

- `click`

- `pytest`

- `_pytest.monkeypatch.notset`

- `click.testing.CliRunner`

- `flask.Blueprint`

- `flask.current_app`

- `flask.Flask`

- `flask.cli.AppGroup`

- `flask.cli.dotenv`

- `flask.cli.find_best_app`

- `flask.cli.FlaskGroup`

- `flask.cli.get_version`

- `flask.cli.load_dotenv`

- `flask.cli.locate_app`

- `flask.cli.NoAppException`

- `flask.cli.prepare_import`

- `flask.cli.run_command`

- `flask.cli.ScriptInfo`

- `flask.cli.with_appcontext`

- `cliapp.app.testapp`

- `flask.__version__`

- `werkzeug.__version__`

- `platform.python_version`



## Functions


### `runner() → None`



- **Line:** 45–46
- **Complexity:** 1
- **Calls:** CliRunner


### `test_cli_name(test_apps) → None`


Make sure the CLI object's name is the app's name and not the app itself


- **Line:** 49–53
- **Complexity:** 2
- **Calls:** none


### `test_find_best_app(test_apps) → None`


Test if `find_best_app` behaves as expected with different combinations of input.


- **Line:** 56–148
- **Complexity:** 14
- **Calls:** ScriptInfo, isinstance, raises, Flask, find_best_app, TypeError


### `create_app() → None`



- **Line:** 77–78
- **Complexity:** 1
- **Calls:** Flask


### `create_app(foo) → None`



- **Line:** 85–86
- **Complexity:** 1
- **Calls:** Flask


### `create_app(foo, script_info) → None`



- **Line:** 93–94
- **Complexity:** 1
- **Calls:** Flask


### `make_app() → None`



- **Line:** 101–102
- **Complexity:** 1
- **Calls:** Flask


### `create_app() → None`



- **Line:** 111–112
- **Complexity:** 1
- **Calls:** Flask


### `create_app() → None`



- **Line:** 120–121
- **Complexity:** 1
- **Calls:** Flask


### `create_app(foo, bar) → None`



- **Line:** 138–139
- **Complexity:** 1
- **Calls:** Flask


### `create_app() → None`



- **Line:** 145–146
- **Complexity:** 1
- **Calls:** TypeError


### `test_prepare_import(request, value, path, result) → None`


Expect the correct path to be set and the correct import and app names
to be returned.

:func:`prepare_exec_for_file` has a side effect where the parent directory
of the given import is added to :data:`sys.path`. This is reset after the
test runs.


- **Line:** 181–197
- **Complexity:** 3
- **Calls:** parametrize, addfinalizer, prepare_import, join


### `reset_path() → None`



- **Line:** 191–192
- **Complexity:** 1
- **Calls:** none


### `test_locate_app(test_apps, iname, aname, result) → None`



- **Line:** 218–221
- **Complexity:** 2
- **Calls:** parametrize, ScriptInfo, locate_app


### `test_locate_app_raises(test_apps, iname, aname) → None`



- **Line:** 242–246
- **Complexity:** 1
- **Calls:** parametrize, ScriptInfo, raises, locate_app


### `test_locate_app_suppress_raise() → None`



- **Line:** 249–256
- **Complexity:** 2
- **Calls:** ScriptInfo, locate_app, raises


### `test_get_version(test_apps, capsys) → None`



- **Line:** 259–276
- **Complexity:** 4
- **Calls:** MockCtx, get_version, readouterr, python_version


### `exit(self) → None`



- **Line:** 268–269
- **Complexity:** 1
- **Calls:** none


### `test_scriptinfo(test_apps, monkeypatch) → None`


Test of ScriptInfo.


- **Line:** 279–326
- **Complexity:** 11
- **Calls:** ScriptInfo, load_app, abspath, raises, chdir, join, Flask, dirname


### `create_app(info) → None`



- **Line:** 299–300
- **Complexity:** 1
- **Calls:** Flask


### `test_with_appcontext(runner) → None`


Test of with_appcontext.


- **Line:** 329–341
- **Complexity:** 3
- **Calls:** command, ScriptInfo, invoke, echo, Flask


### `testcmd() → None`



- **Line:** 334–335
- **Complexity:** 1
- **Calls:** command, echo


### `test_appgroup(runner) → None`


Test of with_appcontext.


- **Line:** 344–371
- **Complexity:** 5
- **Calls:** group, command, ScriptInfo, invoke, echo, Flask


### `cli() → None`



- **Line:** 348–349
- **Complexity:** 1
- **Calls:** group


### `test() → None`



- **Line:** 352–353
- **Complexity:** 1
- **Calls:** command, echo


### `subgroup() → None`



- **Line:** 356–357
- **Complexity:** 1
- **Calls:** group


### `test2() → None`



- **Line:** 360–361
- **Complexity:** 1
- **Calls:** command, echo


### `test_flaskgroup(runner) → None`


Test FlaskGroup.


- **Line:** 374–390
- **Complexity:** 3
- **Calls:** group, command, invoke, Flask, echo


### `create_app(info) → None`



- **Line:** 377–378
- **Complexity:** 1
- **Calls:** Flask


### `cli() → None`



- **Line:** 381–382
- **Complexity:** 1
- **Calls:** group


### `test() → None`



- **Line:** 385–386
- **Complexity:** 1
- **Calls:** command, echo


### `test_flaskgroup_debug(runner, set_debug_flag) → None`


Test FlaskGroup debug flag behavior.


- **Line:** 394–412
- **Complexity:** 3
- **Calls:** parametrize, group, command, invoke, Flask, echo, str


### `create_app(info) → None`



- **Line:** 397–400
- **Complexity:** 1
- **Calls:** Flask


### `cli() → None`



- **Line:** 403–404
- **Complexity:** 1
- **Calls:** group


### `test() → None`



- **Line:** 407–408
- **Complexity:** 1
- **Calls:** command, echo, str


### `test_print_exceptions(runner) → None`


Print the stacktrace if the CLI.


- **Line:** 415–429
- **Complexity:** 4
- **Calls:** group, invoke, Exception, Flask


### `create_app(info) → None`



- **Line:** 418–420
- **Complexity:** 1
- **Calls:** Exception, Flask


### `cli() → None`



- **Line:** 423–424
- **Complexity:** 1
- **Calls:** group


### `invoke(self, runner) → None`



- **Line:** 434–450
- **Complexity:** 1
- **Calls:** FlaskGroup, partial, Flask, route


### `create_app(info) → None`



- **Line:** 435–447
- **Complexity:** 1
- **Calls:** Flask, route


### `yyy_get_post(x, y) → None`



- **Line:** 440–441
- **Complexity:** 1
- **Calls:** route


### `aaa_post() → None`



- **Line:** 444–445
- **Complexity:** 1
- **Calls:** route


### `invoke_no_routes(self, runner) → None`



- **Line:** 453–461
- **Complexity:** 1
- **Calls:** FlaskGroup, partial, Flask


### `create_app(info) → None`



- **Line:** 454–458
- **Complexity:** 1
- **Calls:** Flask


### `expect_order(self, order, output) → None`



- **Line:** 463–467
- **Complexity:** 3
- **Calls:** zip, splitlines, len


### `test_simple(self, invoke) → None`



- **Line:** 469–472
- **Complexity:** 2
- **Calls:** invoke, expect_order


### `test_sort(self, invoke) → None`



- **Line:** 474–489
- **Complexity:** 2
- **Calls:** expect_order, invoke


### `test_all_methods(self, invoke) → None`



- **Line:** 491–495
- **Complexity:** 3
- **Calls:** invoke


### `test_no_routes(self, invoke_no_routes) → None`



- **Line:** 497–500
- **Complexity:** 3
- **Calls:** invoke_no_routes


### `test_load_dotenv(monkeypatch) → None`



- **Line:** 507–526
- **Complexity:** 9
- **Calls:** setenv, chdir, load_dotenv, append, join, getcwd


### `test_dotenv_path(monkeypatch) → None`



- **Line:** 530–537
- **Complexity:** 4
- **Calls:** getcwd, load_dotenv, append, join


### `test_dotenv_optional(monkeypatch) → None`



- **Line:** 540–544
- **Complexity:** 2
- **Calls:** setattr, chdir, load_dotenv


### `test_disable_dotenv_from_env(monkeypatch, runner) → None`



- **Line:** 548–552
- **Complexity:** 2
- **Calls:** chdir, setitem, invoke, FlaskGroup


### `test_run_cert_path() → None`



- **Line:** 555–565
- **Complexity:** 2
- **Calls:** make_context, raises


### `test_run_cert_adhoc(monkeypatch) → None`



- **Line:** 568–582
- **Complexity:** 2
- **Calls:** setitem, make_context, raises, ModuleType


### `test_run_cert_import(monkeypatch) → None`



- **Line:** 585–609
- **Complexity:** 4
- **Calls:** setitem, make_context, raises, object, SSLContext


### `test_run_cert_no_ssl(monkeypatch) → None`



- **Line:** 612–615
- **Complexity:** 1
- **Calls:** setattr, raises, make_context


### `test_cli_blueprints(app) → None`


Test blueprint commands register correctly to the application


- **Line:** 618–658
- **Complexity:** 5
- **Calls:** Blueprint, command, register_blueprint, test_cli_runner, invoke, echo


### `custom_command() → None`



- **Line:** 626–627
- **Complexity:** 1
- **Calls:** command, echo


### `nested_command() → None`



- **Line:** 630–631
- **Complexity:** 1
- **Calls:** command, echo


### `merged_command() → None`



- **Line:** 634–635
- **Complexity:** 1
- **Calls:** command, echo


### `late_command() → None`



- **Line:** 638–639
- **Complexity:** 1
- **Calls:** command, echo


### `test_cli_empty(app) → None`


If a Blueprint's CLI group is empty, do not register it.


- **Line:** 661–667
- **Complexity:** 2
- **Calls:** Blueprint, register_blueprint, invoke, test_cli_runner



## Classes


### `Module`



- **Bases:** none
- **Methods:** none


### `Module`



- **Bases:** none
- **Methods:** none


### `Module`



- **Bases:** none
- **Methods:** none


### `Module`



- **Bases:** none
- **Methods:** create_app


### `Module`



- **Bases:** none
- **Methods:** create_app


### `Module`



- **Bases:** none
- **Methods:** create_app


### `Module`



- **Bases:** none
- **Methods:** make_app


### `Module`



- **Bases:** none
- **Methods:** create_app


### `Module`



- **Bases:** none
- **Methods:** create_app


### `Module`



- **Bases:** none
- **Methods:** none


### `Module`



- **Bases:** none
- **Methods:** none


### `Module`



- **Bases:** none
- **Methods:** create_app


### `Module`



- **Bases:** none
- **Methods:** create_app


### `MockCtx`



- **Bases:** object
- **Methods:** exit


### `TestRoutes`



- **Bases:** none
- **Methods:** invoke, invoke_no_routes, expect_order, test_simple, test_sort, test_all_methods, test_no_routes

