from pyczmq._cffi import C, ffi, cdef

__doc__ = """
The zsys class provides miscellaneous functions. Only a limited set of
functions are exposed from the czmq zsys module as many duplicate
functionality of built-in python types or libraries.
"""

@cdef('void zsys_version (int *major, int *minor, int *patch);')
def zsys_version():
    """
    Returns the tuple (major, minor, patch) of the current czmq version.
    """
    major = ffi.new('int*')
    minor= ffi.new('int*')
    patch = ffi.new('int*')
    C.zsys_version(major, minor, patch)
    return (major[0], minor[0], patch[0])
