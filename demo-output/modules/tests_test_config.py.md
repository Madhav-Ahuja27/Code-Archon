# Module: `tests/test_config.py`

**Path:** `C:\temp\flask\tests\test_config.py`
**Lines:** 202
**Avg Complexity:** 3.2


## Description

tests.test_config
~~~~~~~~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `os`

- `textwrap`

- `datetime.timedelta`

- `pytest`

- `flask`

- `flask._compat.PY2`



## Functions


### `common_object_test(app) → None`



- **Line:** 24–27
- **Complexity:** 4
- **Calls:** none


### `test_config_from_file() → None`



- **Line:** 30–33
- **Complexity:** 1
- **Calls:** Flask, from_pyfile, common_object_test, rsplit


### `test_config_from_object() → None`



- **Line:** 36–39
- **Complexity:** 1
- **Calls:** Flask, from_object, common_object_test


### `test_config_from_json() → None`



- **Line:** 42–46
- **Complexity:** 1
- **Calls:** Flask, dirname, from_json, common_object_test, abspath, join


### `test_config_from_mapping() → None`



- **Line:** 49–64
- **Complexity:** 1
- **Calls:** Flask, from_mapping, common_object_test, raises


### `test_config_from_class() → None`



- **Line:** 67–76
- **Complexity:** 1
- **Calls:** Flask, from_object, common_object_test


### `test_config_from_envvar(monkeypatch) → None`



- **Line:** 79–91
- **Complexity:** 4
- **Calls:** setattr, Flask, from_envvar, common_object_test, raises, str, rsplit


### `test_config_from_envvar_missing(monkeypatch) → None`



- **Line:** 94–104
- **Complexity:** 4
- **Calls:** setattr, str, startswith, endswith, raises, Flask, from_envvar


### `test_config_missing() → None`



- **Line:** 107–116
- **Complexity:** 4
- **Calls:** Flask, str, startswith, endswith, raises, from_pyfile


### `test_config_missing_json() → None`



- **Line:** 119–128
- **Complexity:** 4
- **Calls:** Flask, str, startswith, endswith, raises, from_json


### `test_custom_config_class() → None`



- **Line:** 131–141
- **Complexity:** 2
- **Calls:** Flask, isinstance, from_object, common_object_test


### `test_session_lifetime() → None`



- **Line:** 144–147
- **Complexity:** 2
- **Calls:** Flask


### `test_send_file_max_age() → None`



- **Line:** 150–155
- **Complexity:** 3
- **Calls:** Flask, timedelta


### `test_get_namespace() → None`



- **Line:** 158–181
- **Complexity:** 13
- **Calls:** Flask, get_namespace, len


### `test_from_pyfile_weird_encoding(tmpdir, encoding) → None`



- **Line:** 185–202
- **Complexity:** 3
- **Calls:** parametrize, join, write_binary, Flask, from_pyfile, encode, str, decode, dedent, format



## Classes


### `Base`



- **Bases:** object
- **Methods:** none


### `Test`



- **Bases:** Base
- **Methods:** none


### `Config`



- **Bases:** flask.Config
- **Methods:** none


### `Flask`



- **Bases:** flask.Flask
- **Methods:** none

