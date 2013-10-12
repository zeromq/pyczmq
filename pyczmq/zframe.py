from __future__ import print_function
from pyczmq._cffi import C, cdef, ptop, ffi

__doc__ = """
The zframe class provides methods to send and receive single message
frames across 0MQ sockets. A frame corresponds to one zmq_msg_t. When
you read a frame from a socket, the zframe_more() method indicates if
the frame is part of an unfinished multipart message. The zframe_send
method normally destroys the frame, but with the ZFRAME_REUSE flag,
you can send the same frame many times. Frames are binary, and this
class has no special support for text data.
"""


cdef('typedef struct _zframe_t zframe_t;')


MORE = 1
REUSE = 2
DONTWAIT = 4


@cdef('void zframe_destroy (zframe_t **self_p);')
def destroy(frame):
    """Destroy a frame
    """
    return C.zframe_destroy(ptop('zframe_t', frame))


@cdef('zframe_t * zframe_new (const void *data, size_t size);')
def new(data):
    """Create a new frame with optional size, and optional data
    """
    return C.zframe_new(data, len(data))


@cdef('zframe_t * zframe_new_empty (void);')
def new_empty():
    """Create an empty (zero-sized) frame
    """
    return C.zframe_new_empty()


@cdef('zframe_t * zframe_recv (void *socket);')
def recv(sock):
    """
    Receive frame from socket, returns zframe_t object or NULL if the recv
    was interrupted. Does a blocking recv, if you want to not block then use
    zframe_recv_nowait().
    """
    return  C.zframe_recv(sock)


@cdef('zframe_t * zframe_recv_nowait (void *socket);')
def recv_nowait(sock):
    """
    Receive a new frame off the socket. Returns newly allocated frame, or
    NULL if there was no input waiting, or if the read was interrupted.
    """
    return  C.zframe_recv_nowait(sock)


@cdef('int zframe_send (zframe_t **self_p, void *socket, int flags);')
def send(frame, socket, flags):
    """
    Send a frame to a socket, destroy frame after sending.
    Return -1 on error, 0 on success.
    """
    return C.zframe_send(frame, socket, flags)


@cdef('size_t zframe_size (zframe_t *self);')
def size(frame):
    """Return number of bytes in frame data
    """
    return C.zframe_size(frame)


@cdef('void * zframe_data (zframe_t *self);')
def data(frame):
    """Return address of frame data
    """
    return ffi.buffer(C.zframe_data(frame), C.zframe_size(frame))


@cdef('zframe_t * zframe_dup (zframe_t *self);')
def dup(frame):
    """Create a new frame that duplicates an existing frame
    """
    return C.zframe_dup(frame)


@cdef('char * zframe_strhex (zframe_t *self);', returns_string=True)
def strhex(frame):
    """Return frame data encoded as printable hex string
    """
    return C.zframe_strhex(frame)


@cdef('char * zframe_strdup (zframe_t *self);')
def strdup(frame):
    """Return frame data copied into freshly allocated string
    """
    return C.zframe_strdup(frame)


@cdef('bool zframe_streq (zframe_t *self, const char *string);')
def streq(frame, string):
    """Return TRUE if frame body is equal to string, excluding terminator
    """
    return  C.zframe_streq(frame, string)


@cdef('int zframe_more (zframe_t *self);')
def more(frame):
    """
    Return frame MORE indicator (1 or 0), set when reading frame from
    socket or by the zframe_set_more() method
    """
    return  C.zframe_more(frame)


@cdef('void zframe_set_more (zframe_t *self, int more);')
def set_more(frame, more):
    """
    Set frame MORE indicator (1 or 0). Note this is NOT used when sending 
    frame to socket, you have to specify flag explicitly.
    """
    return C.zframe_set_more(frame, more)


@cdef('bool zframe_eq (zframe_t *self, zframe_t *other);')
def eq(frame, other):
    """
    Return TRUE if two frames have identical size and data
    If either frame is NULL, equality is always false.
    """
    return  C.zframe_eq(frame, other)


@cdef('void zframe_reset (zframe_t *self, const void *data, size_t size);')
def reset(frame, string):
    """Set new contents for frame
    """
    return  C.zframe_reset(frame, string, len(string))

