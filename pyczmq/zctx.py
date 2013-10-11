from pyczmq._cffi import C, ffi, cdef, ptop


cdef('typedef struct _zctx_t zctx_t;')


@cdef('void zctx_destroy (zctx_t **self_p);')
def destroy(ctx):
    """
    Destroy context and all sockets in it
    """
    return C.zctx_destroy(ptop('zctx_t', ctx))


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
