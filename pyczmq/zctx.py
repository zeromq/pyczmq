from pyczmq._cffi import C, ffi, cdef, ptop

__doc__ = """
The zctx class wraps 0MQ contexts. It manages open sockets in the
context and automatically closes these before terminating the
context. It provides a simple way to set the linger timeout on
sockets, and configure contexts for number of I/O threads. Sets-up
signal (interrupt) handling for the process.

The zctx class has these main features:

  - Tracks all open sockets and automatically closes them before
    calling zmq_term(). This avoids an infinite wait on open sockets.

  - Automatically configures sockets with a ZMQ_LINGER timeout you can
    define, and which defaults to zero. The default behavior of zctx
    is therefore like 0MQ/2.0, immediate termination with loss of any
    pending messages. You can set any linger timeout you like by
    calling the zctx_set_linger() method.

  - Moves the iothreads configuration to a separate method, so that
    default usage is 1 I/O thread. Lets you configure this value.
    Sets up signal (SIGINT and SIGTERM) handling so that blocking
    calls such as zmq_recv() and zmq_poll() will return when the user
    presses Ctrl-C.
"""


cdef('typedef struct _zctx_t zctx_t;')


@cdef('void zctx_destroy (zctx_t **self_p);')
def destroy(ctx):
    """
    Destroy context and all sockets in it
    """
    #if ctx is not ffi.NULL:
    C.zctx_destroy(ptop('zctx_t', ctx))
    #return ffi.NULL


@cdef('zctx_t * zctx_new (void);')
def new():
    """
    Create new context.
    """
    return ffi.gc(C.zctx_new(), destroy)


@cdef('void zctx_set_iothreads (zctx_t *self, int iothreads);')
def set_iothreads(ctx, iothreads):
    """
    Raise default I/O threads from 1, for crazy heavy applications
    The rule of thumb is one I/O thread per gigabyte of traffic in
    or out. Call this method before creating any sockets on the context
    or the setting will have no effect.
    """
    return C.zctx_set_iothreads(ctx, iothreads)


@cdef('void zctx_set_linger (zctx_t *self, int linger);')
def set_linger(ctx, linger):
    """
    Set msecs to flush sockets when closing them, see the ZMQ_LINGER
    man page section for more details. By default, set to zero, so
    any in-transit messages are discarded when you destroy a socket or
    a context.
    """
    return C.zctx_set_linger(ctx, linger)


@cdef('void zctx_set_pipehwm (zctx_t *self, int pipehwm);')
def set_pipehwm(ctx, pipehwm):
    """
    Set initial high-water mark for inter-thread pipe sockets. Note that
    this setting is separate from the default for normal sockets. You
    should change the default for pipe sockets *with care*. Too low values
    will cause blocked threads, and an infinite setting can cause memory
    exhaustion. The default, no matter the underlying ZeroMQ version, is
    1,000.
    """
    return C.zctx_set_pipehwm(ctx, pipehwm)


@cdef('void zctx_set_sndhwm (zctx_t *self, int sndhwm);')
def set_sndhwm(ctx, sndhwm):
    """
    Set initial send HWM for all new normal sockets created in context.
    You can set this per-socket after the socket is created.
    The default, no matter the underlying ZeroMQ version, is 1,000.
    """
    return C.zctx_set_sndhwm(ctx, sndhwm)


@cdef('void zctx_set_rcvhwm (zctx_t *self, int rcvhwm);')
def set_rcvhwm(ctx, rcvhwm):
    """
    Set initial receive HWM for all new normal sockets created in context.
    You can set this per-socket after the socket is created.
    The default, no matter the underlying ZeroMQ version, is 1,000.
    """
    return C.zctx_set_rcvhwm(ctx, rcvhwm)


@cdef('void * zctx_underlying (zctx_t *self);', nullable=True)
def underlying(ctx):
    """
    Return low-level 0MQ context object, will be NULL before first socket
    is created. Use with care.
    """
    return C.zctx_underlying(ctx)


cdef('extern volatile int zctx_interrupted;')
"""
Global signal indicator, TRUE when user presses Ctrl-C or the process
gets a SIGTERM signal.
"""
interrupted = C.zctx_interrupted


cdef('int zctx_test (bool verbose);')
