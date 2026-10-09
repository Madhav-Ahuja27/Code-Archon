# Module: `src/flask/config.py`

**Path:** `C:\temp\flask\src\flask\config.py`
**Lines:** 269
**Avg Complexity:** 3.4


## Description

flask.config
~~~~~~~~~~~~

Implements the configuration related objects.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `errno`

- `os`

- `types`

- `werkzeug.utils.import_string`

- `json`

- `_compat.iteritems`

- `_compat.string_types`



## Functions


### `__init__(self, name, get_converter) → None`



- **Line:** 25–27
- **Complexity:** 2
- **Calls:** none


### `__get__(self, obj, type) → None`



- **Line:** 29–35
- **Complexity:** 3
- **Calls:** get_converter


### `__set__(self, obj, value) → None`



- **Line:** 37–38
- **Complexity:** 1
- **Calls:** none


### `__init__(self, root_path, defaults) → None`



- **Line:** 85–87
- **Complexity:** 2
- **Calls:** __init__


### `from_envvar(self, variable_name, silent) → None`


Loads a configuration from an environment variable pointing to
a configuration file.  This is basically just a shortcut with nicer
error messages for this line of code::

    app.config.from_pyfile(os.environ['YOURAPPLICATION_SETTINGS'])

:param variable_name: name of the environment variable
:param silent: set to ``True`` if you want silent failure for missing
               files.
:return: bool. ``True`` if able to load config, ``False`` otherwise.


- **Line:** 89–111
- **Complexity:** 3
- **Calls:** get, from_pyfile, RuntimeError


### `from_pyfile(self, filename, silent) → None`


Updates the values in the config from a Python file.  This function
behaves as if the file was imported as module with the
:meth:`from_object` function.

:param filename: the filename of the config.  This can either be an
                 absolute filename or a filename relative to the
                 root path.
:param silent: set to ``True`` if you want silent failure for missing
               files.

.. versionadded:: 0.7
   `silent` parameter.


- **Line:** 113–139
- **Complexity:** 4
- **Calls:** join, ModuleType, from_object, open, exec, compile, read


### `from_object(self, obj) → None`


Updates the values from the given object.  An object can be of one
of the following two types:

-   a string: in this case the object with that name will be imported
-   an actual object reference: that object is used directly

Objects are usually either modules or classes. :meth:`from_object`
loads only the uppercase attributes of the module/class. A ``dict``
object will not work with :meth:`from_object` because the keys of a
``dict`` are not attributes of the ``dict`` class.

Example of module-based configuration::

    app.config.from_object('yourapplication.default_config')
    from yourapplication import default_config
    app.config.from_object(default_config)

Nothing is done to the object before loading. If the object is a
class and has ``@property`` attributes, it needs to be
instantiated before being passed to this method.

You should not use this function to load the actual configuration but
rather configuration defaults.  The actual config should be loaded
with :meth:`from_pyfile` and ideally from a location not within the
package because the package might be installed system wide.

See :ref:`config-dev-prod` for an example of class-based configuration
using :meth:`from_object`.

:param obj: an import name or object


- **Line:** 141–177
- **Complexity:** 4
- **Calls:** isinstance, dir, import_string, isupper, getattr


### `from_json(self, filename, silent) → None`


Updates the values in the config from a JSON file. This function
behaves as if the JSON object was a dictionary and passed to the
:meth:`from_mapping` function.

:param filename: the filename of the JSON file.  This can either be an
                 absolute filename or a filename relative to the
                 root path.
:param silent: set to ``True`` if you want silent failure for missing
               files.

.. versionadded:: 0.11


- **Line:** 179–202
- **Complexity:** 4
- **Calls:** join, from_mapping, open, loads, read


### `from_mapping(self) → None`


Updates the config like :meth:`update` ignoring items with non-upper
keys.

.. versionadded:: 0.11


- **Line:** 204–225
- **Complexity:** 7
- **Calls:** append, len, hasattr, items, TypeError, isupper


### `get_namespace(self, namespace, lowercase, trim_namespace) → None`


Returns a dictionary containing a subset of configuration options
that match the specified namespace/prefix. Example usage::

    app.config['IMAGE_STORE_TYPE'] = 'fs'
    app.config['IMAGE_STORE_PATH'] = '/var/app/images'
    app.config['IMAGE_STORE_BASE_URL'] = 'http://img.website.com'
    image_store_config = app.config.get_namespace('IMAGE_STORE_')

The resulting dictionary `image_store_config` would look like::

    {
        'type': 'fs',
        'path': '/var/app/images',
        'base_url': 'http://img.website.com'
    }

This is often useful when configuration options map directly to
keyword arguments in functions or class constructors.

:param namespace: a configuration namespace
:param lowercase: a flag indicating if the keys of the resulting
                  dictionary should be lowercase
:param trim_namespace: a flag indicating if the keys of the resulting
                  dictionary should not include the namespace

.. versionadded:: 0.11


- **Line:** 227–266
- **Complexity:** 5
- **Calls:** iteritems, startswith, lower, len


### `__repr__(self) → None`



- **Line:** 268–269
- **Complexity:** 1
- **Calls:** __repr__



## Classes


### `ConfigAttribute`


Makes an attribute forward to the config


- **Bases:** object
- **Methods:** __init__, __get__, __set__


### `Config`


Works exactly like a dict but provides ways to fill it from files
or special dictionaries.  There are two common patterns to populate the
config.

Either you can fill the config from a config file::

    app.config.from_pyfile('yourconfig.cfg')

Or alternatively you can define the configuration options in the
module that calls :meth:`from_object` or provide an import path to
a module that should be loaded.  It is also possible to tell it to
use the same module and with that provide the configuration values
just before the call::

    DEBUG = True
    SECRET_KEY = 'development key'
    app.config.from_object(__name__)

In both cases (loading from any Python file or loading from modules),
only uppercase keys are added to the config.  This makes it possible to use
lowercase values in the config file for temporary values that are not added
to the config or to define the config keys in the same file that implements
the application.

Probably the most interesting way to load configurations is from an
environment variable pointing to a file::

    app.config.from_envvar('YOURAPPLICATION_SETTINGS')

In this case before launching the application you have to set this
environment variable to the file you want to use.  On Linux and OS X
use the export statement::

    export YOURAPPLICATION_SETTINGS='/path/to/config/file'

On windows use `set` instead.

:param root_path: path to which files are read relative from.  When the
                  config object is created by the application, this is
                  the application's :attr:`~flask.Flask.root_path`.
:param defaults: an optional dictionary of default values


- **Bases:** dict
- **Methods:** __init__, from_envvar, from_pyfile, from_object, from_json, from_mapping, get_namespace, __repr__

