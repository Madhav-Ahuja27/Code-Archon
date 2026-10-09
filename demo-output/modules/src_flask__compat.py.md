# Module: `src/flask/_compat.py`

**Path:** `C:\temp\flask\src\flask\_compat.py`
**Lines:** 145
**Avg Complexity:** 1.5


## Description

flask._compat
~~~~~~~~~~~~~

Some py2/py3 compatibility support based on a stripped down
version of six so we don't have to depend on a specific version
of it.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `sys`

- `inspect.getfullargspec`

- `io.StringIO`

- `collections.abc`

- `inspect.getargspec`

- `cStringIO.StringIO`

- `collections`

- `os.fspath`

- `warnings`



## Functions


### `reraise(tp, value, tb) → None`



- **Line:** 36–39
- **Complexity:** 2
- **Calls:** with_traceback


### `implements_to_string(cls) → None`



- **Line:** 54–57
- **Complexity:** 1
- **Calls:** encode, __unicode__


### `with_metaclass(meta) → None`


Create a base class with a metaclass.


- **Line:** 60–69
- **Complexity:** 1
- **Calls:** __new__, meta


### `__new__(metacls, name, this_bases, d) → None`



- **Line:** 66–67
- **Complexity:** 1
- **Calls:** meta


### `__enter__(self) → None`



- **Line:** 87–88
- **Complexity:** 1
- **Calls:** none


### `__exit__(self) → None`



- **Line:** 90–93
- **Complexity:** 2
- **Calls:** hasattr, exc_clear


### `fspath(path) → None`



- **Line:** 114–115
- **Complexity:** 2
- **Calls:** hasattr, __fspath__


### `__init__(self, name, version, value) → None`



- **Line:** 119–123
- **Complexity:** 1
- **Calls:** format


### `_warn(self) → None`



- **Line:** 125–128
- **Complexity:** 1
- **Calls:** warn


### `__eq__(self, other) → None`



- **Line:** 130–132
- **Complexity:** 1
- **Calls:** _warn


### `__ne__(self, other) → None`



- **Line:** 134–136
- **Complexity:** 1
- **Calls:** _warn


### `__bool__(self) → None`



- **Line:** 138–140
- **Complexity:** 1
- **Calls:** _warn



## Classes


### `metaclass`



- **Bases:** type
- **Methods:** __new__


### `_Mgr`



- **Bases:** object
- **Methods:** __enter__, __exit__


### `_DeprecatedBool`



- **Bases:** object
- **Methods:** __init__, _warn, __eq__, __ne__, __bool__

