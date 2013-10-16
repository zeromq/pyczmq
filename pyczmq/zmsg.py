from pyczmq._cffi import C, ffi, ptop, cdef

__doc__ = """
The zmsg class provides methods to send and receive multipart messages
across 0MQ sockets. This class provides a list-like container
interface, with methods to work with the overall container. zmsg_t
messages are composed of zero or more zframe_t frames.
"""


cdef('typedef struct _zmsg_t zmsg_t;')


@cdef('void zmsg_destroy (zmsg_t **self_p);')
def destroy(m):
    """Destroy a message object and all frames it contains
    """
    C.zmsg_destroy(ptop('zmsg_t', m))

@cdef('zmsg_t * zmsg_new (void);')
def new():
    """Create a new empty message object,

    Note, no gc wrapper, messages self-destruct by send.  If you don't
    send a message, you DO have to destroy() it.
    """
    return C.zmsg_new()


@cdef('zmsg_t * zmsg_recv (void *socket);', nullable=True)
def recv(socket):
    """
    Receive message from socket, returns zmsg_t object or NULL if the recv
    was interrupted. Does a blocking recv, if you want to not block then use
    the zloop class or zmq_poll to check for socket input before receiving.
    """
    return C.zmsg_recv(socket)


@cdef('int zmsg_send (zmsg_t **self_p, void *socket);')
def send(m, socket):
    """
    Send message to socket, destroy after sending. If the message has no
    frames, sends nothing but destroys the message anyhow. Safe to call
    if zmsg is null.
    """
    return C.zmsg_send(ptop('zmsg_t', m), socket)


@cdef('size_t zmsg_size (zmsg_t *self);')
def size(msg):
    """Return size of message, i.e. number of frames (0 or more).
    """
    return C.zmsg_size(msg)



@cdef('size_t zmsg_content_size (zmsg_t *self);')
def content_size(msg):
    """
    Return total size of all frames in message.
    """
    return  C.zmsg_content_size(msg)


@cdef('int zmsg_push (zmsg_t *self, zframe_t *frame);')
def push(msg, frame):
    """
    Push frame to the front of the message, i.e. before all other frames.
    Message takes ownership of frame, will destroy it when message is sent.
    Returns 0 on success, -1 on error.
    """
    return C.zmsg_push(msg, frame)


@cdef('zframe_t * zmsg_pop (zmsg_t *self);')
def pop(msg):
    """
    Remove first frame from message, if any. Returns frame, or NULL. Caller
    now owns frame and must destroy it when finished with it.
    """
    return C.zmsg_pop(msg)


@cdef('int zmsg_append (zmsg_t *self, zframe_t **frame_p);')
def append(m, f):
    """
    Add frame to the end of the message, i.e. after all other frames.
    Message takes ownership of frame, will destroy it when message is sent.
    Returns 0 on success. Deprecates zmsg_add, which did not nullify the
    caller's frame reference.
    """
    return C.zmsg_append(m, ptop('zframe_t', f))


@cdef('int zmsg_pushstr (zmsg_t *self, const char *format, ...);')
def pushstr(msg, fmt):
    """
    Push string as new frame to front of message.
    Returns 0 on success, -1 on error.
    """
    return C.zmsg_pushstr(msg, fmt)


@cdef('int zmsg_addstr (zmsg_t *self, const char *format, ...);')
def addstr(msg, fmt):
    """
    Push string as new frame to end of message.
    Returns 0 on success, -1 on error.
    """
    return C.zmsg_addstr(msg, fmt)


@cdef('char * zmsg_popstr (zmsg_t *self);', nullable=True, returns_string=True)
def popstr(msg):
    """
    Pop frame off front of message, return as fresh string. If there were
    no more frames in the message, returns NULL.
    """
    return C.zmsg_popstr(msg)


@cdef('void zmsg_wrap (zmsg_t *self, zframe_t *frame);')
def wrap(msg, frame):
    """
    Push frame plus empty frame to front of message, before first frame.
    Message takes ownership of frame, will destroy it when message is sent.
    """
    return C.zmsg_wrap(msg, frame)


@cdef('zframe_t * zmsg_unwrap (zmsg_t *self);')
def unwrap(msg):
    """
    Pop frame off front of message, caller now owns frame
    If next frame is empty, pops and destroys that empty frame.
    """
    return C.zmsg_unwrap(msg)


@cdef('void zmsg_remove (zmsg_t *self, zframe_t *frame);')
def remove(msg, frame):
    """Remove specified frame from list, if present. Does not destroy frame.
    """
    return C.zmsg_remove(msg, frame)


@cdef('zframe_t * zmsg_first (zmsg_t *self);', nullable=True)
def first(msg):
    """
    Set cursor to first frame in message. Returns frame, or NULL, if the
    message is empty. Use this to navigate the frames as a list.
    """
    return C.zmsg_first(msg)


@cdef('zframe_t * zmsg_next (zmsg_t *self);', nullable=True)
def next(msg):
    """
    Return the next frame. If there are no more frames, returns NULL. To move
    to the first frame call zmsg_first(). Advances the cursor.
    """
    return C.zmsg_next(msg)


@cdef('zframe_t * zmsg_last (zmsg_t *self);', nullable=True)
def last(msg):
    """Return the last frame. If there are no frames, returns NULL.
    """
    return C.zmsg_last(msg)


@cdef('int zmsg_save (zmsg_t *self, FILE *file);')
def save(msg, filename):
    """
    Save message to an open file, return 0 if OK, else -1. The message is
    saved as a series of frames, each with length and data. Note that the
    file is NOT guaranteed to be portable between operating systems, not
    versions of CZMQ. The file format is at present undocumented and liable
    to arbitrary change.
    """
    return C.zmsg_save(msg, filename)


@cdef('zmsg_t * zmsg_load (zmsg_t *self, FILE *file);', nullable=True)
def load(msg, filename):
    """
    Load/append an open file into message, create new message if
    null message provided. Returns NULL if the message could not
    be loaded.
    """
    return C.zmsg_load(msg, filename)


@cdef('zmsg_t * zmsg_dup (zmsg_t *self);', nullable=True)
def dup(msg):
    """
    Create copy of message, as new message object. Returns a fresh zmsg_t
    object, or NULL if there was not enough heap memory.
    """
    return C.zmsg_dup(msg)
