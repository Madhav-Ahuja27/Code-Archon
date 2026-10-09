# Module: `tests/test_json_tag.py`

**Path:** `C:\temp\flask\tests\test_json_tag.py`
**Lines:** 93
**Avg Complexity:** 2.2


## Description

tests.test_json_tag
~~~~~~~~~~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `datetime.datetime`

- `uuid.uuid4`

- `pytest`

- `flask.Markup`

- `flask.json.tag.JSONTag`

- `flask.json.tag.TaggedJSONSerializer`



## Functions


### `test_dump_load_unchanged(data) → None`



- **Line:** 34–36
- **Complexity:** 2
- **Calls:** parametrize, TaggedJSONSerializer, loads, Markup, uuid4, replace, dumps, utcnow


### `test_duplicate_tag() → None`



- **Line:** 39–47
- **Complexity:** 3
- **Calls:** TaggedJSONSerializer, raises, register, isinstance


### `test_custom_tag() → None`



- **Line:** 50–70
- **Complexity:** 2
- **Calls:** TaggedJSONSerializer, register, isinstance, tag, Foo, loads, dumps


### `__init__(self, data) → None`



- **Line:** 52–53
- **Complexity:** 1
- **Calls:** none


### `check(self, value) → None`



- **Line:** 59–60
- **Complexity:** 1
- **Calls:** isinstance


### `to_json(self, value) → None`



- **Line:** 62–63
- **Complexity:** 1
- **Calls:** tag


### `to_python(self, value) → None`



- **Line:** 65–66
- **Complexity:** 1
- **Calls:** Foo


### `test_tag_interface() → None`



- **Line:** 73–77
- **Complexity:** 1
- **Calls:** JSONTag, raises


### `test_tag_order() → None`



- **Line:** 80–93
- **Complexity:** 3
- **Calls:** TaggedJSONSerializer, register, isinstance



## Classes


### `TagDict`



- **Bases:** JSONTag
- **Methods:** none


### `Foo`



- **Bases:** object
- **Methods:** __init__


### `TagFoo`



- **Bases:** JSONTag
- **Methods:** check, to_json, to_python


### `Tag1`



- **Bases:** JSONTag
- **Methods:** none


### `Tag2`



- **Bases:** JSONTag
- **Methods:** none

