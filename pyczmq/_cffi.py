from cffi import FFI

ffi = FFI()
C = ffi.dlopen('czmq')
