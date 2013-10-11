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
    def wraps(f):
        def inner_f(*args):
            val = f(*args)
            if returns_string:
                return ffi.string(val)
            if nullable and val == ffi.NULL:
                return None
            return val
        return inner_f
    return wraps

