from cffi import FFI

ffi = FFI()
C = ffi.dlopen('czmq')

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

