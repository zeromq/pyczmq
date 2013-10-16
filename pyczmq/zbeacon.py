from pyczmq._cffi import C, ffi, ptop, cdef

__doc__ = """
The zbeacon class implements a peer-to-peer discovery service for
local networks. A beacon can broadcast and/or capture service
announcements using UDP messages on the local area network. This
implementation uses IPv4 UDP broadcasts. You can define the format of
your outgoing beacons, and set a filter that validates incoming
beacons. Beacons are sent and received asynchronously in the
background. The zbeacon API provides a incoming beacons on a ZeroMQ
socket (the pipe) that you can configure, poll on, and receive
messages on. Incoming beacons are always delivered as two frames: the
ipaddress of the sender (a string), and the beacon data itself
(binary, as published).
"""

cdef('typedef struct _zbeacon_t zbeacon_t;')


@cdef('void zbeacon_destroy (zbeacon_t **self_p);')
def destroy(beacon):
    """Destroy a beacon
    """
    C.zbeacon_destroy(ptop('zbeacon_t', beacon))


@cdef('zbeacon_t * zbeacon_new (int port_nbr);')
def new(port):
    """Create a new beacon on a certain UDP port
    """
    return ffi.gc(C.zbeacon_new(port), destroy)


@cdef('char * zbeacon_hostname (zbeacon_t *self);', returns_string=True)
def hostname(beacon):
    """Returns the hostname string for this beacon's interface
    """
    return C.zbeacon_hostname(beacon)


@cdef('void zbeacon_set_interval (zbeacon_t *self, int interval);')
def set_interval(beacon, interval):
    """Set broadcast interval in milliseconds (default is 1000 msec)
    """
    return C.zbeacon_set_interval(beacon, interval)


@cdef('void zbeacon_noecho (zbeacon_t *self);')
def noecho(beacon):
    """Filter out any beacon that looks exactly like ours
    """
    return C.zbeacon_noecho(beacon)


@cdef('void zbeacon_publish (zbeacon_t *self, void *transmit, size_t size);')
def publish(beacon, string):
    """Start broadcasting beacon to peers at the specified interval"""
    return C.zbeacon_publish(beacon, string, len(string))


@cdef('void zbeacon_silence (zbeacon_t *self);')
def silence(beacon):
    """Stop broadcasting beacons
    """
    return C.zbeacon_silence(beacon)


@cdef('void zbeacon_subscribe (zbeacon_t *self, char *filter, size_t size);')
def subscribe(beacon, string):
    """Start listening to other peers; zero-sized filter means get everything
    """
    return C.zbeacon_subscribe(beacon, string, len(string))


@cdef('void zbeacon_unsubscribe (zbeacon_t *self);')
def unsubscribe(beacon):
    """Stop listening to other peers
    """
    return C.zbeacon_unsubscribe(beacon)


@cdef('void * zbeacon_socket (zbeacon_t *self);')
def socket(beacon):
    """Get beacon ZeroMQ socket, for polling or receiving messages
    """
    return C.zbeacon_socket(beacon)


cdef('void zbeacon_test (bool verbose);')
