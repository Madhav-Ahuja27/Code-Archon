# Module: `src/flask/json/tag.py`

**Path:** `C:\temp\flask\src\flask\json\tag.py`
**Lines:** 309
**Avg Complexity:** 2.2


## Description

Tagged JSON
~~~~~~~~~~~

A compact representation for lossless serialization of non-standard JSON types.
:class:`~flask.sessions.SecureCookieSessionInterface` uses this to serialize
the session data, but it may be useful in other places. It can be extended to
support other types.

.. autoclass:: TaggedJSONSerializer
    :members:

.. autoclass:: JSONTag
    :members:

Let's seen an example that adds support for :class:`~collections.OrderedDict`.
Dicts don't have an order in Python or JSON, so to handle this we will dump
the items as a list of ``[key, value]`` pairs. Subclass :class:`JSONTag` and
give it the new key ``' od'`` to identify the type. The session serializer
processes dicts first, so insert the new tag at the front of the order since
``OrderedDict`` must be processed before ``dict``. ::

    from flask.json.tag import JSONTag

    class TagOrderedDict(JSONTag):
        __slots__ = ('serializer',)
        key = ' od'

        def check(self, value):
            return isinstance(value, OrderedDict)

        def to_json(self, value):
            return [[k, self.serializer.tag(v)] for k, v in iteritems(value)]

        def to_python(self, value):
            return OrderedDict(value)

    app.session_interface.serializer.register(TagOrderedDict, index=0)

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `base64.b64decode`

- `base64.b64encode`

- `datetime.datetime`

- `uuid.UUID`

- `jinja2.Markup`

- `werkzeug.http.http_date`

- `werkzeug.http.parse_date`

- `_compat.iteritems`

- `_compat.text_type`

- `json.dumps`

- `json.loads`



## Functions


### `__init__(self, serializer) → None`


Create a tagger for the given serializer.


- **Line:** 68–70
- **Complexity:** 2
- **Calls:** none


### `check(self, value) → None`


Check if the given value should be tagged by this tag.


- **Line:** 72–74
- **Complexity:** 1
- **Calls:** none


### `to_json(self, value) → None`


Convert the Python object to an object that is a valid JSON type.
The tag will be added later.


- **Line:** 76–79
- **Complexity:** 1
- **Calls:** none


### `to_python(self, value) → None`


Convert the JSON representation back to the correct type. The tag
will already be removed.


- **Line:** 81–84
- **Complexity:** 1
- **Calls:** none


### `tag(self, value) → None`


Convert the value to a valid JSON type and add the tag structure
around it.


- **Line:** 86–89
- **Complexity:** 3
- **Calls:** to_json


### `check(self, value) → None`



- **Line:** 102–107
- **Complexity:** 1
- **Calls:** isinstance, len, next, iter


### `to_json(self, value) → None`



- **Line:** 109–111
- **Complexity:** 1
- **Calls:** next, iter, tag


### `to_python(self, value) → None`



- **Line:** 113–115
- **Complexity:** 1
- **Calls:** next, iter


### `check(self, value) → None`



- **Line:** 121–122
- **Complexity:** 1
- **Calls:** isinstance


### `to_json(self, value) → None`



- **Line:** 124–127
- **Complexity:** 1
- **Calls:** dict, tag, iteritems


### `check(self, value) → None`



- **Line:** 136–137
- **Complexity:** 1
- **Calls:** isinstance


### `to_json(self, value) → None`



- **Line:** 139–140
- **Complexity:** 1
- **Calls:** tag


### `to_python(self, value) → None`



- **Line:** 142–143
- **Complexity:** 1
- **Calls:** tuple


### `check(self, value) → None`



- **Line:** 149–150
- **Complexity:** 1
- **Calls:** isinstance


### `to_json(self, value) → None`



- **Line:** 152–153
- **Complexity:** 1
- **Calls:** tag


### `check(self, value) → None`



- **Line:** 162–163
- **Complexity:** 1
- **Calls:** isinstance


### `to_json(self, value) → None`



- **Line:** 165–166
- **Complexity:** 1
- **Calls:** decode, b64encode


### `to_python(self, value) → None`



- **Line:** 168–169
- **Complexity:** 1
- **Calls:** b64decode


### `check(self, value) → None`



- **Line:** 180–181
- **Complexity:** 1
- **Calls:** callable, getattr


### `to_json(self, value) → None`



- **Line:** 183–184
- **Complexity:** 1
- **Calls:** text_type, __html__


### `to_python(self, value) → None`



- **Line:** 186–187
- **Complexity:** 1
- **Calls:** Markup


### `check(self, value) → None`



- **Line:** 194–195
- **Complexity:** 1
- **Calls:** isinstance


### `to_json(self, value) → None`



- **Line:** 197–198
- **Complexity:** 1
- **Calls:** none


### `to_python(self, value) → None`



- **Line:** 200–201
- **Complexity:** 1
- **Calls:** UUID


### `check(self, value) → None`



- **Line:** 208–209
- **Complexity:** 1
- **Calls:** isinstance


### `to_json(self, value) → None`



- **Line:** 211–212
- **Complexity:** 1
- **Calls:** http_date


### `to_python(self, value) → None`



- **Line:** 214–215
- **Complexity:** 1
- **Calls:** parse_date


### `__init__(self) → None`



- **Line:** 248–253
- **Complexity:** 2
- **Calls:** register


### `register(self, tag_class, force, index) → None`


Register a new tag with this serializer.

:param tag_class: tag class to register. Will be instantiated with this
    serializer instance.
:param force: overwrite an existing tag. If false (default), a
    :exc:`KeyError` is raised.
:param index: index to insert the new tag in the tag order. Useful when
    the new tag is a special case of an existing tag. If ``None``
    (default), the tag is appended to the end of the order.

:raise KeyError: if the tag key is already registered and ``force`` is
    not true.


- **Line:** 255–281
- **Complexity:** 5
- **Calls:** tag_class, append, insert, KeyError, format


### `tag(self, value) → None`


Convert a value to a tagged representation if necessary.


- **Line:** 283–289
- **Complexity:** 3
- **Calls:** check, tag


### `untag(self, value) → None`


Convert a tagged representation back to the original type.


- **Line:** 291–301
- **Complexity:** 3
- **Calls:** next, to_python, len, iter


### `dumps(self, value) → None`


Tag the value and dump it to a compact JSON string.


- **Line:** 303–305
- **Complexity:** 1
- **Calls:** dumps, tag


### `loads(self, value) → None`


Load data from a JSON string and deserialized any tagged objects.


- **Line:** 307–309
- **Complexity:** 1
- **Calls:** loads



## Classes


### `JSONTag`


Base class for defining type tags for :class:`TaggedJSONSerializer`.


- **Bases:** object
- **Methods:** __init__, check, to_json, to_python, tag


### `TagDict`


Tag for 1-item dicts whose only key matches a registered tag.

Internally, the dict key is suffixed with `__`, and the suffix is removed
when deserializing.


- **Bases:** JSONTag
- **Methods:** check, to_json, to_python


### `PassDict`



- **Bases:** JSONTag
- **Methods:** check, to_json


### `TagTuple`



- **Bases:** JSONTag
- **Methods:** check, to_json, to_python


### `PassList`



- **Bases:** JSONTag
- **Methods:** check, to_json


### `TagBytes`



- **Bases:** JSONTag
- **Methods:** check, to_json, to_python


### `TagMarkup`


Serialize anything matching the :class:`~flask.Markup` API by
having a ``__html__`` method to the result of that method. Always
deserializes to an instance of :class:`~flask.Markup`.


- **Bases:** JSONTag
- **Methods:** check, to_json, to_python


### `TagUUID`



- **Bases:** JSONTag
- **Methods:** check, to_json, to_python


### `TagDateTime`



- **Bases:** JSONTag
- **Methods:** check, to_json, to_python


### `TaggedJSONSerializer`


Serializer that uses a tag system to compactly represent objects that
are not JSON types. Passed as the intermediate serializer to
:class:`itsdangerous.Serializer`.

The following extra types are supported:

* :class:`dict`
* :class:`tuple`
* :class:`bytes`
* :class:`~flask.Markup`
* :class:`~uuid.UUID`
* :class:`~datetime.datetime`


- **Bases:** object
- **Methods:** __init__, register, tag, untag, dumps, loads

