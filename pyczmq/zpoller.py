from pyczmq._cffi import C, ffi


ffi.cdef('typedef struct _zpoller_t zpoller_t;')


ffi.cdef('void zpoller_destroy (zpoller_t **self_p);')
def destroy(poller):
    """Destroy a poller"""
    C.zpoller_destroy(ptop('zpoller_t', poller))


ffi.cdef('zpoller_t * zpoller_new (void *reader, ...);')
def new(*readers):
    """Create new poller"""
    return ffi.gc(C.zpoller_new(*readers), destroy)


ffi.cdef(' void * zpoller_wait (zpoller_t *self, int timeout);')
def wait(poller, timeout):
    """
    Poll the registered readers for I/O, return first socket that has input.
    This means the order that sockets are defined in the poll list affects
    their priority. If you need a balanced poll, use the low level zmq_poll
    method directly.
    """
    return C.zpoller_wait(poller, timeout)


ffi.cdef('bool zpoller_expired (zpoller_t *self);')
def expired(poller):
    """
    Return true if the last zpoller_wait () call ended because the timeout
    expired, without any error.
    """
    return C.zpoller_expired(poller)


ffi.cdef('bool zpoller_terminated (zpoller_t *self);')
def terminated(poller):
    """
    Return true if the last zpoller_wait () call ended because the process
    was interrupted, or the parent context was destroyed.
    """
    return C.zpoller_terminated(poller)


ffi.cdef('int zpoller_test (bool verbose);')

