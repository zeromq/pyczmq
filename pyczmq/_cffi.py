import inspect
from functools import wraps
from cffi import FFI

ffi = FFI()
C = ffi.dlopen('czmq')
Z = ffi.dlopen('zmq')

def nullable(func):
    def inner(*args):
        val = func(*args)
        if val == ffi.NULL:
            return None
        return val
    return inner


def ptop(typ, val):
    ptop = ffi.new('%s*[1]' % typ)
    ptop[0] = val
    return ptop


def tostr(func):
    def inner(*args):
        return ffi.string(func(*args))
    return inner


def cdef(decl, returns_string=False, nullable=False):
    ffi.cdef(decl)
    def wrap(f):
        @wraps(f)
        def inner_f(*args):
            val = f(*args)
            if nullable and val == ffi.NULL:
                return None
            elif returns_string:
                return ffi.string(val)
            return val

        args, varargs, varkw, defaults = inspect.getargspec(f)
        defaults = () if defaults is None else defaults
        defaults = ["\"{}\"".format(a) if type(a) == str else a for a in defaults]
        l = ["{}={}".format(arg, defaults[(idx+1)*-1]) 
             if len(defaults)-1 >= idx else 
             arg for idx, arg in enumerate(reversed(list(args)))]
        if varargs:
            l.append('*' + varargs)
        if varkw:
            l.append('**' + varkw)
        doc = "{}({})\n{}".format(f.__name__, ', '.join(reversed(l)), f.__doc__)
        inner_f.__doc__ = doc
        return inner_f
    return wrap


