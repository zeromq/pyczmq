from pyczmq._cffi import C, ffi, cdef

__doc__ = """
The zstr class provides utility functions for sending and receiving
strings across 0MQ sockets. It sends strings without a terminating
null, and appends a null byte on received strings. This class is for
simple message sending.
"""


@cdef('char * zstr_recv (void *socket);', returns_string=True)
def recv(sock):
    """
    Receive a string off a socket, caller must free it
    """
    return C.zstr_recv(sock)


@cdef('char * zstr_recv_nowait (void *socket);', returns_string=True)
def recv_nowait(sock):
    """
    Receive a string off a socket if socket had input waiting
    """
    return C.zstr_recv_nowait(sock)


@cdef('int zstr_send (void *socket, const char *format, ...);')
def send(sock, fmt):
    """
    Send a formatted string to a socket
    """
    C.zstr_send(sock, fmt)


@cdef('int zstr_sendm (void *socket, const char *format, ...);')
def sendm(sock, fmt):
    """
    Send a formatted string to a socket, with MORE flag
    """
    return C.zstr_sendm(sock, fmt)


@cdef('int zstr_sendx (void *socket, const char *string, ...);')
def sendx(sock, string):
    """
    Send a series of strings (until NULL) as multipart data
    Returns 0 if the strings could be sent OK, or -1 on error.
    """
    return C.zstr_sendx(sock, string)


@cdef('int zstr_recvx (void *socket, char **string_p, ...);')
def recvx(sock, string_p):
    """
    Receive a series of strings (until NULL) from multipart data
    Each string is allocated and filled with string data; if there
    are not enough frames, unallocated strings are set to NULL.
    Returns -1 if the message could not be read, else returns the
    number of strings filled, zero or more.
    """
    return C.zstr_recvx(sock, string_p)


cdef('int zstr_test (bool verbose);')
