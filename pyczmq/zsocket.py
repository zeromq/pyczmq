from pyczmq._cffi import C, ffi, cdef

__doc__ = """
The zsocket class provides helper functions for 0MQ sockets. It
doesn't wrap the 0MQ socket type, to avoid breaking all libzmq
socket-related calls.
"""

@cdef('void zsocket_destroy (zctx_t *self, void *socket);')
def destroy(ctx, socket):
    """Destroy a socket within our CZMQ context.

    'pyczmq.zsocket.new' automatically registers this destructor with
    the garbage collector, so this is normally not necessary to use,
    unless you need to destroy sockets created by some other means
    (like a call directly to 'pyczmq.C.zsocket_new')
    """
    return C.zsocket_destroy(ctx, socket)


@cdef('void * zsocket_new (zctx_t *self, int type);')
def new(ctx, typ):
    """
    Create a new socket within our CZMQ context, replaces zmq_socket.
    Use this to get automatic management of the socket at shutdown.
    Note: SUB sockets do not automatically subscribe to everything;
    you must set filters explicitly.
    """
    return ffi.gc(C.zsocket_new(ctx, typ), lambda s: destroy(ctx, s))


@cdef('int zsocket_bind (void *socket, const char *format, ...);')
def bind(sock, fmt):
    """
    Bind a socket to a formatted endpoint. If the port is specified as
    '*', binds to any free port from ZSOCKET_DYNFROM to ZSOCKET_DYNTO
    and returns the actual port number used. Otherwise asserts that
    the bind succeeded with the specified port number. Always returns
    the port number if successful.
    """
    return C.zsocket_bind(sock, fmt)


@cdef('int zsocket_unbind (void *socket, const char *format, ...);')
def unbind(sock, fmt):
    """
    Unbind a socket from a formatted endpoint.  Returns 0 if OK, -1 if
    the endpoint was invalid or the function isn't supported.
    """
    return C.zsocket_unbind(sock, fmt)


@cdef('int zsocket_connect (void *socket, const char *format, ...);')
def connect(sock, fmt):
    """
    Connect a socket to a formatted endpoint Returns 0 if OK, -1 if
    the endpoint was invalid.
    """
    return C.zsocket_connect(sock, fmt)


@cdef('int zsocket_disconnect (void *socket, const char *format, ...);')
def disconnect(sock, fmt):
    """
    Disonnect a socket from a formatted endpoint Returns 0 if OK, -1
    if the endpoint was invalid or the function isn't supported.
    """
    return C.zsocket_disconnect(sock, fmt)


@cdef('bool zsocket_poll (void *socket, int msecs);')
def poll(sock, msecs):
    """
    Poll for input events on the socket. Returns TRUE if there is input
    ready on the socket, else FALSE.
    """
    return C.zsocket_poll(sock, msecs)


@cdef('char * zsocket_type_str (void *socket);')
def type_str(sock):
    """Returns socket type as printable constant string"""
    return C.zsocket_type_str(sock)
