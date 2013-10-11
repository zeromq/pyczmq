from pyczmq._cffi import C, ffi, ptop, tostr


ffi.cdef('typedef struct _zbeacon_t zbeacon_t;')


ffi.cdef('void zbeacon_destroy (zbeacon_t **self_p);')
def destroy(beacon):
    """Destroy a beacon
    """
    C.zbeacon_destroy(ptop('zbeacon_t', beacon))


ffi.cdef('zbeacon_t * zbeacon_new (int port_nbr);')
def new(port):
    """Create a new beacon on a certain UDP port
    """
    return ffi.gc(C.zbeacon_new(port), destroy)


ffi.cdef('char * zbeacon_hostname (zbeacon_t *self);')
@tostr
def hostname(beacon):
    return C.zbeacon_hostname(beacon)


ffi.cdef('void zbeacon_set_interval (zbeacon_t *self, int interval);')
def interval(beacon, interval):
    """Set broadcast interval in milliseconds (default is 1000 msec)
    """
    return C.zbeacon_set_interval(beacon, interval)


ffi.cdef('void zbeacon_noecho (zbeacon_t *self);')
def noecho(beacon):
    """Filter out any beacon that looks exactly like ours
    """
    return C.zbeacon_noecho(beacon)


ffi.cdef('void zbeacon_publish (zbeacon_t *self, char *transmit, size_t size);')
def publish(beacon, string):
    """Start broadcasting beacon to peers at the specified interval"""
    return C.zbeacon_publish(beacon, string, len(string))


ffi.cdef('void zbeacon_silence (zbeacon_t *self);')
def silence(beacon):
    """Stop broadcasting beacons
    """
    return C.zbeacon_silence(beacon)


ffi.cdef('void zbeacon_subscribe (zbeacon_t *self, char *filter, size_t size);')
def subscribe(beacon, string):
    """Start listening to other peers; zero-sized filter means get everything
    """
    return C.zbeacon_subscribe(beacon, string, len(string))


ffi.cdef('void zbeacon_unsubscribe (zbeacon_t *self);')
def unsubscribe(beacon):
    """Stop listening to other peers
    """
    return C.zbeacon_unsubscribe(beacon)


ffi.cdef('void * zbeacon_socket (zbeacon_t *self);')
def socket(beacon):
    """Get beacon ZeroMQ socket, for polling or receiving messages
    """
    return C.zbeacon_socket(beacon)


ffi.cdef('void zbeacon_test (bool verbose);')
