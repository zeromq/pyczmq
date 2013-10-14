from pyczmq._cffi import ffi, C, ptop, cdef

__doc__ = """
The zloop class provides an event-driven reactor pattern. The reactor
handles zmq_pollitem_t items (pollers or writers, sockets or fds), and
once-off or repeated timers. Its resolution is 1 msec. It uses a
tickless timer to reduce CPU interrupts in inactive processes.
"""


cdef('typedef struct _zloop_t zloop_t;')
cdef('typedef int (zloop_fn) (zloop_t *loop, zmq_pollitem_t *item, void *arg);')


@cdef('void zloop_destroy (zloop_t **self_p);')
def destroy(loop):
    """
    Destroy a reactor, this is not necessary if you create it with
    new.
    """
    if loop is not ffi.NULL:
        C.zloop_destroy(ptop('zloop_t', loop))
    return ffi.NULL


@cdef(' zloop_t * zloop_new (void);')
def new():
    """Create a new zloop reactor"""
    return C.zloop_new()


@cdef('int zloop_poller (zloop_t *self, zmq_pollitem_t *item,'
         ' zloop_fn handler, void *arg);')
def poller(p, item, handler, arg=None):
    """
    Register pollitem with the reactor. When the pollitem is ready, will call
    the handler, passing the arg. Returns 0 if OK, -1 if there was an error.
    If you register the pollitem more than once, each instance will invoke its
    corresponding handler.

    """
    return C.zloop_poller(p, item, handler, ffi.new_handle(arg))


@cdef('void zloop_poller_end (zloop_t *self, zmq_pollitem_t *item);')
def poller_end(loop, item):
    """
    Cancel a pollitem from the reactor, specified by socket or FD. If both
    are specified, uses only socket. If multiple poll items exist for same
    socket/FD, cancels ALL of them.
    """
    return C.zloop_poller_end(loop, item)


@cdef('void zloop_set_tolerant (zloop_t *self, zmq_pollitem_t *item);')
def set_tolerant(loop, item):
    """
    Configure a registered pollitem to ignore errors. If you do not set this,
    then pollitems that have errors are removed from the reactor silently.
    """
    return C.zloop_set_tolerant(loop, item)


@cdef('int zloop_timer (zloop_t *self, size_t delay, size_t times, zloop_fn handler, void *arg);')
def timer(loop, delay, times, handler, arg):
    """
    Register a timer that expires after some delay and repeats some number of
    times. At each expiry, will call the handler, passing the arg. To
    run a timer forever, use 0 times. Returns 0 if OK, -1 if there was an
    error.
    """
    return C.zloop_timer(loop, delay, times, handler, arg)


@cdef('int zloop_timer_end (zloop_t *self, void *arg);')
def timer_end(loop, arg):
    """
    Cancel all timers for a specific argument (as provided in zloop_timer)
    """
    return C.zloop_timer_end(loop, arg)


@cdef('void zloop_set_verbose (zloop_t *self, bool verbose);')
def set_verbose(loop, verbose):
    """
    Set verbose tracing of reactor on/off
    """
    return C.zloop_set_verbose(loop, verbose)


@cdef('int zloop_start (zloop_t *self);')
def start(loop):
    """
    Start the reactor. Takes control of the thread and returns when the 0MQ
    context is terminated or the process is interrupted, or any event handler
    returns -1. Event handlers may register new sockets and timers, and
    cancel sockets. Returns 0 if interrupted, -1 if cancelled by a handler.
    """
    return C.zloop_start(loop)


cdef('void zloop_test (bool verbose);')

