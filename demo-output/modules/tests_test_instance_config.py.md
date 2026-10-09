# Module: `tests/test_instance_config.py`

**Path:** `C:\temp\flask\tests\test_instance_config.py`
**Lines:** 144
**Avg Complexity:** 2.1


## Description

tests.test_instance
~~~~~~~~~~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `os`

- `sys`

- `pytest`

- `flask`

- `flask._compat.PY2`

- `main_app.app`

- `config_module_app.app`

- `config_package_app.app`

- `site_app.app`

- `installed_package.app`

- `site_package`

- `site_egg`

- `unimportable`



## Functions


### `test_explicit_instance_paths(modules_tmpdir) → None`



- **Line:** 18–24
- **Complexity:** 3
- **Calls:** Flask, raises, str


### `test_main_module_paths(modules_tmpdir, purge_module) → None`



- **Line:** 28–36
- **Complexity:** 2
- **Calls:** xfail, join, write, purge_module, abspath, getcwd


### `test_uninstalled_module_paths(modules_tmpdir, purge_module) → None`



- **Line:** 39–50
- **Complexity:** 2
- **Calls:** write, purge_module, str, join


### `test_uninstalled_package_paths(modules_tmpdir, purge_module) → None`



- **Line:** 53–66
- **Complexity:** 2
- **Calls:** mkdir, join, write, purge_module, str


### `test_installed_module_paths(modules_tmpdir, modules_tmpdir_prefix, purge_module, site_packages, limit_loader) → None`



- **Line:** 69–79
- **Complexity:** 2
- **Calls:** write, purge_module, join


### `test_installed_package_paths(limit_loader, modules_tmpdir, modules_tmpdir_prefix, purge_module, monkeypatch) → None`



- **Line:** 82–97
- **Complexity:** 2
- **Calls:** mkdir, syspath_prepend, join, write, purge_module


### `test_prefix_package_paths(limit_loader, modules_tmpdir, modules_tmpdir_prefix, purge_module, site_packages) → None`



- **Line:** 100–112
- **Complexity:** 2
- **Calls:** mkdir, join, write, purge_module


### `test_egg_installed_paths(install_egg, modules_tmpdir, modules_tmpdir_prefix) → None`



- **Line:** 115–128
- **Complexity:** 3
- **Calls:** write, install_egg, join, str, mkdir


### `test_meta_path_loader_without_is_package(request, modules_tmpdir) → None`



- **Line:** 132–144
- **Complexity:** 1
- **Calls:** skipif, join, write, append, addfinalizer, Loader, raises


### `find_module(self, name, path) → None`



- **Line:** 137–138
- **Complexity:** 1
- **Calls:** none



## Classes


### `Loader`



- **Bases:** object
- **Methods:** find_module

