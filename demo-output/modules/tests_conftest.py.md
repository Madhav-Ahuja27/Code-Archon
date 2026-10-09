# Module: `tests/conftest.py`

**Path:** `C:\temp\flask\tests\conftest.py`
**Lines:** 202
**Avg Complexity:** 1.3


## Description

tests.conftest
~~~~~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `os`

- `pkgutil`

- `sys`

- `textwrap`

- `pytest`

- `_pytest.monkeypatch`

- `flask`

- `flask.Flask`

- `subprocess`



## Functions


### `_standard_os_environ() → None`


Set up ``os.environ`` at the start of the test session to have
standard values. Returns a list of operations that is used by
:func:`._reset_os_environ` after each test.


- **Line:** 22–43
- **Complexity:** 3
- **Calls:** fixture, MonkeyPatch, undo, delenv, setenv


### `_reset_os_environ(monkeypatch, _standard_os_environ) → None`


Reset ``os.environ`` to the standard environ after each test,
in case a test changed something without cleaning up.


- **Line:** 47–51
- **Complexity:** 1
- **Calls:** fixture, extend


### `app() → None`



- **Line:** 60–62
- **Complexity:** 1
- **Calls:** Flask, dirname


### `app_ctx(app) → None`



- **Line:** 66–68
- **Complexity:** 1
- **Calls:** app_context


### `req_ctx(app) → None`



- **Line:** 72–74
- **Complexity:** 1
- **Calls:** test_request_context


### `client(app) → None`



- **Line:** 78–79
- **Complexity:** 1
- **Calls:** test_client


### `test_apps(monkeypatch) → None`



- **Line:** 83–86
- **Complexity:** 1
- **Calls:** syspath_prepend, abspath, join, dirname


### `leak_detector() → None`



- **Line:** 90–98
- **Complexity:** 3
- **Calls:** fixture, append, pop


### `limit_loader(request, monkeypatch) → None`


Patch pkgutil.get_loader to give loader without get_filename or archive.

This provides for tests where a system has custom loaders, e.g. Google App
Engine's HardenedModulesHook, which have neither the `get_filename` method
nor the `archive` attribute.

This fixture will run the testcase twice, once with and once without the
limitation/mock.


- **Line:** 102–130
- **Complexity:** 2
- **Calls:** fixture, setattr, LimitedLoader, getattr, old_get_loader, AttributeError


### `__init__(self, loader) → None`



- **Line:** 116–117
- **Complexity:** 1
- **Calls:** none


### `__getattr__(self, name) → None`



- **Line:** 119–123
- **Complexity:** 1
- **Calls:** getattr, AttributeError


### `get_loader() → None`



- **Line:** 127–128
- **Complexity:** 1
- **Calls:** LimitedLoader, old_get_loader


### `modules_tmpdir(tmpdir, monkeypatch) → None`


A tmpdir added to sys.path.


- **Line:** 134–138
- **Complexity:** 1
- **Calls:** mkdir, syspath_prepend, str


### `modules_tmpdir_prefix(modules_tmpdir, monkeypatch) → None`



- **Line:** 142–144
- **Complexity:** 1
- **Calls:** setattr, str


### `site_packages(modules_tmpdir, monkeypatch) → None`


Create a fake site-packages.


- **Line:** 148–156
- **Complexity:** 1
- **Calls:** mkdir, syspath_prepend, str, format


### `install_egg(modules_tmpdir, monkeypatch) → None`


Generate egg from package name inside base and put the egg into
sys.path.


- **Line:** 160–194
- **Complexity:** 1
- **Calls:** ensure_dir, ensure, join, write, check_call, listdir, syspath_prepend, isinstance, ValueError, dedent, str, format


### `inner(name, base) → None`



- **Line:** 164–192
- **Complexity:** 1
- **Calls:** ensure_dir, ensure, join, write, check_call, listdir, syspath_prepend, isinstance, ValueError, dedent, str, format


### `purge_module(request) → None`



- **Line:** 198–202
- **Complexity:** 1
- **Calls:** addfinalizer, pop


### `inner(name) → None`



- **Line:** 199–200
- **Complexity:** 1
- **Calls:** addfinalizer, pop



## Classes


### `Flask`



- **Bases:** _Flask
- **Methods:** none


### `LimitedLoader`



- **Bases:** object
- **Methods:** __init__, __getattr__

