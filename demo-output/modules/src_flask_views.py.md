# Module: `src/flask/views.py`

**Path:** `C:\temp\flask\src\flask\views.py`
**Lines:** 163
**Avg Complexity:** 5.0


## Description

flask.views
~~~~~~~~~~~

This module provides class-based views inspired by the ones in Django.

:copyright: 2010 Pallets
:license: BSD-3-Clause



## Imports



- `_compat.with_metaclass`

- `globals.request`



## Functions


### `dispatch_request(self) → None`


Subclasses have to override this method to implement the
actual view function code.  This method is called with all
the arguments from the URL rule.


- **Line:** 69–74
- **Complexity:** 4
- **Calls:** NotImplementedError


### `as_view(cls, name) → None`


Converts the class into an actual view function that can be used
with the routing system.  Internally this generates a function on the
fly which will instantiate the :class:`View` on each request and call
the :meth:`dispatch_request` method on it.

The arguments passed to :meth:`as_view` are forwarded to the
constructor of the class.


- **Line:** 77–108
- **Complexity:** 3
- **Calls:** view_class, dispatch_request, decorator


### `view() → None`



- **Line:** 87–89
- **Complexity:** 1
- **Calls:** view_class, dispatch_request


### `__init__(cls, name, bases, d) → None`



- **Line:** 116–135
- **Complexity:** 7
- **Calls:** __init__, set, super, getattr, hasattr, update, add, upper


### `dispatch_request(self) → None`



- **Line:** 154–163
- **Complexity:** 4
- **Calls:** getattr, meth, lower



## Classes


### `View`


Alternative way to use view functions.  A subclass has to implement
:meth:`dispatch_request` which is called with the view arguments from
the URL routing system.  If :attr:`methods` is provided the methods
do not have to be passed to the :meth:`~flask.Flask.add_url_rule`
method explicitly::

    class MyView(View):
        methods = ['GET']

        def dispatch_request(self, name):
            return 'Hello %s!' % name

    app.add_url_rule('/hello/<name>', view_func=MyView.as_view('myview'))

When you want to decorate a pluggable view you will have to either do that
when the view function is created (by wrapping the return value of
:meth:`as_view`) or you can use the :attr:`decorators` attribute::

    class SecretView(View):
        methods = ['GET']
        decorators = [superuser_required]

        def dispatch_request(self):
            ...

The decorators stored in the decorators list are applied one after another
when the view function is created.  Note that you can *not* use the class
based decorators since those would decorate the view class and not the
generated view function!


- **Bases:** object
- **Methods:** dispatch_request, as_view


### `MethodViewType`


Metaclass for :class:`MethodView` that determines what methods the view
defines.


- **Bases:** type
- **Methods:** __init__


### `MethodView`


A class-based view that dispatches request methods to the corresponding
class methods. For example, if you implement a ``get`` method, it will be
used to handle ``GET`` requests. ::

    class CounterAPI(MethodView):
        def get(self):
            return session.get('counter', 0)

        def post(self):
            session['counter'] = session.get('counter', 0) + 1
            return 'OK'

    app.add_url_rule('/counter', view_func=CounterAPI.as_view('counter'))


- **Bases:** with_metaclass(MethodViewType, View)
- **Methods:** dispatch_request

