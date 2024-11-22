import contextvars
import inspect
_in__init__ = contextvars.ContextVar('_immutable_in__init__', default=False)

class _Immutable:
    """Immutable mixin class"""
    __slots__ = ()

    def __setattr__(self, name, value):
        if _in__init__.get() is not self:
            raise TypeError("object doesn't support attribute assignment")
        else:
            super().__setattr__(name, value)

    def __delattr__(self, name):
        if _in__init__.get() is not self:
            raise TypeError("object doesn't support attribute assignment")
        else:
            super().__delattr__(name)

def immutable(f):
    """A decorator which makes the returned object immutable.
    
    The object has to inherit from the _Immutable class for this to work.
    """
    def wrapped(self, *args, **kwargs):
        token = _in__init__.set(self)
        try:
            return f(self, *args, **kwargs)
        finally:
            _in__init__.reset(token)
    return wrapped