from pyczmq._cffi import ffi, Z, cdef

IO_THREADS = 1
MAX_SOCKETS = 2

IO_THREADS_DFLT = 1
MAX_SOCKETS_DFLT = 1024

POLLIN = 1
POLLOUT = 2
POLLERR = 4

EVENT_CONNECTED = 1
EVENT_CONNECT_DELAYED = 2
EVENT_CONNECT_RETRIED = 4

EVENT_LISTENING = 8
EVENT_BIND_FAILED = 16

EVENT_ACCEPTED = 32
EVENT_ACCEPT_FAILED = 64

EVENT_CLOSED = 128
EVENT_CLOSE_FAILED = 256
EVENT_DISCONNECTED = 512
EVENT_MONITOR_STOPPED = 1024

EVENT_ALL = (EVENT_CONNECTED | EVENT_CONNECT_DELAYED | 
             EVENT_CONNECT_RETRIED | EVENT_LISTENING | 
             EVENT_BIND_FAILED | EVENT_ACCEPTED | 
             EVENT_ACCEPT_FAILED | EVENT_CLOSED | 
             EVENT_CLOSE_FAILED | EVENT_DISCONNECTED | 
             EVENT_MONITOR_STOPPED)

PAIR = 0
PUB = 1
SUB = 2
REQ = 3
REP = 4
DEALER = 5
ROUTER = 6
PULL = 7
PUSH = 8
XPUB = 9
XSUB = 10
STREAM = 11

types = dict(
    PAIR=PAIR,
    PUB=PUB,
    SUB=SUB,
    REQ=REQ,
    REP=REP,
    DEALER=DEALER,
    ROUTER=ROUTER,
    PULL=PULL,
    PUSH=PUSH,
    XPUB=XPUB,
    XSUB=XSUB,
    STREAM=STREAM)

AFFINITY = 4
IDENTITY = 5
SUBSCRIBE = 6
UNSUBSCRIBE = 7
RATE = 8
RECOVERY_IVL = 9
SNDBUF = 11
RCVBUF = 12
RCVMORE = 13
FD = 14
EVENTS = 15
TYPE = 16
LINGER = 17
RECONNECT_IVL = 18
BACKLOG = 19
RECONNECT_IVL_MAX = 21
MAXMSGSIZE = 22
SNDHWM = 23
RCVHWM = 24
MULTICAST_HOPS = 25
RCVTIMEO = 27
SNDTIMEO = 28
LAST_ENDPOINT = 32
ROUTER_MANDATORY = 33
TCP_KEEPALIVE = 34
TCP_KEEPALIVE_CNT = 35
TCP_KEEPALIVE_IDLE = 36
TCP_KEEPALIVE_INTVL = 37
TCP_ACCEPT_FILTER = 38
IMMEDIATE = 39
XPUB_VERBOSE = 40
ROUTER_RAW = 41
IPV6 = 42
MECHANISM = 43
PLAIN_SERVER = 44
PLAIN_USERNAME = 45
PLAIN_PASSWORD = 46
CURVE_SERVER = 47
CURVE_PUBLICKEY = 48
CURVE_SECRETKEY = 49
CURVE_SERVERKEY = 50
PROBE_ROUTER = 51
REQ_CORRELATE = 52
REQ_RELAXED = 53
CONFLATE = 54
ZAP_DOMAIN = 55

MORE = 1

DONTWAIT = 1
SNDMORE = 2

NULL = 0
PLAIN = 1
CURVE = 2


@cdef('int zmq_errno (void);')
def errno():
    """
    This function retrieves the errno as it is known to 0MQ
    library. The goal of this function is to make the code 100%
    portable, including where 0MQ compiled with certain CRT library
    (on Windows) is linked to an application that uses different CRT
    library.
    """
    return Z.zmq_errno()


@cdef('void zmq_version (int *major, int *minor, int *patch);')
def version():
    """Returns the tuple (major, minor, patch) of the current zmq
    version.
    """
    major = ffi.new('int*')
    minor= ffi.new('int*')
    patch = ffi.new('int*')
    Z.zmq_version(major, minor, patch)
    return (major[0], minor[0], patch[0])


@cdef('const char *zmq_strerror (int errnum);')
def strerror(num):
    """
    Resolves system errors and 0MQ errors to human-readable string.
    """
    return Z.zmq_strerror(num)


@cdef('void *zmq_ctx_new (void);')
def ctx_new():
    return Z.zmq_ctx_new()


@cdef('int zmq_ctx_term (void *context);')
def ctx_term(ctx):
    return Z.zmq_ctx_term(ctx)


@cdef('int zmq_ctx_shutdown (void *ctx_);')
def ctx_shutdown(ctx):
    return Z.zmq_ctx_shutdown(ctx)


@cdef('int zmq_ctx_set (void *context, int option, int optval);')
def ctx_set(ctx, opt, val):
    return Z.zmq_ctx_set(ctx, opt, val)


@cdef('int zmq_ctx_get (void *context, int option);')
def ctx_get(ctx, opt):
    return Z.zmq_ctx_get(ctx, opt)


@cdef('''
typedef struct zmq_msg_t {unsigned char _ [32];} zmq_msg_t;

typedef void (zmq_free_fn) (void *data, void *hint);
''')


@cdef('int zmq_msg_init (zmq_msg_t *msg);')
def msg_init(msg):
    return Z.zmq_msg_init(msg)


@cdef('int zmq_msg_init_size (zmq_msg_t *msg, size_t size);')
def msg_init_size(msg, size):
    return Z.zmq_msg_init_size(msg, size)


@cdef('int zmq_msg_init_data (zmq_msg_t *msg, void *data,'
         ' size_t size, zmq_free_fn *ffn, void *hint);')
def msg_init_data(msg, data, size, ffn, hint):
    return Z.zmq_msg_init_data(msg, data, size, ffn, hint)


@cdef('int zmq_msg_send (zmq_msg_t *msg, void *s, int flags);')
def msg_send(msg, s, flags):
    return Z.zmq_msg_send(msg, s, flags)


@cdef('int zmq_msg_recv (zmq_msg_t *msg, void *s, int flags);')
def msg_recv(msg, s, flags):
    return Z.zmq_msg_recv(msg, s, flags)


@cdef('int zmq_msg_close (zmq_msg_t *msg);')
def msg_close(msg):
    return Z.zmq_msg_close(msg)


@cdef('int zmq_msg_move (zmq_msg_t *dest, zmq_msg_t *src);')
def msg_move(dest, src):
    return Z.zmq_msg_move(dest, src)


@cdef('int zmq_msg_copy (zmq_msg_t *dest, zmq_msg_t *src);')
def msg_copy(dest, src):
    return Z.zmq_msg_copy(dest, src)


@cdef('void *zmq_msg_data (zmq_msg_t *msg);')
def msg_data(msg):
    return Z.zmq_msg_data(msg)


@cdef('size_t zmq_msg_size (zmq_msg_t *msg);')
def msg_size(msg):
    return Z.zmq_msg_size(msg)


@cdef('int zmq_msg_more (zmq_msg_t *msg);')
def msg_more(msg):
    return Z.zmq_msg_more(msg)


@cdef('int zmq_msg_get (zmq_msg_t *msg, int option);')
def msg_get(msg, opt):
    return Z.zmq_msg_get(msg, opt)


@cdef('int zmq_msg_set (zmq_msg_t *msg, int option, int optval);')
def msg_set(msg, opt, val):
    return Z.zmq_msg_set(msg, opt, val)


cdef('''
typedef struct {
    uint16_t event;
    int32_t  value;
} zmq_event_t;
''')


@cdef('void *zmq_socket (void *ctx, int type);')
def socket(ctx, typ):
    return Z.zmq_socket(ctx, typ)


@cdef('int zmq_close (void *sock);')
def close(sock):
    return Z.zmq_close(sock)


@cdef('int zmq_setsockopt (void *s, int option,'
         ' const void *optval, size_t optvallen);')
def setsockopt(sock, opt, val, len):
    return Z.zmq_setsockopt(sock, opt, val, len)


@cdef('int zmq_getsockopt (void *s, int option,'
         ' void *optval, size_t *optvallen);')
def getsockopt(sock, opt, val, len):
    return Z.zmq_getsockopt(sock, opt, val, len)


@cdef('int zmq_bind (void *s, const char *addr);')
def bind(sock, addr):
    return Z.zmq_bind(sock, addr)


@cdef('int zmq_connect (void *s, const char *addr);')
def connect(sock, addr):
    return Z.zmq_connect(sock, addr)


@cdef('int zmq_unbind (void *s, const char *addr);')
def unbind(sock, addr):
    return Z.zmq_unbind(sock, addr)


@cdef('int zmq_disconnect (void *s, const char *addr);')
def disconnect(sock, addr):
    return Z.zmq_disconnect(sock, addr)


@cdef('int zmq_send (void *s, const void *buf, size_t len, int flags);')
def send(sock, buf, len, flags):
    return Z.zmq_send(sock, buf, len, flags)


@cdef('int zmq_send_const (void *s, const void *buf, size_t len, int flags);')


@cdef('int zmq_recv (void *s, void *buf, size_t len, int flags);')
def recv(sock, buf, len, flags):
    return Z.zmq_recv(sock, buf, len, flags)


@cdef('int zmq_socket_monitor (void *s, const char *addr, int events);')
def socket_monitor(sock, addr, events):
    return Z.zmq_socket_monitor(sock, addr, events)


@cdef('int zmq_sendmsg (void *s, zmq_msg_t *msg, int flags);')
def sendmsg(sock, msg, flags):
    return Z.zmq_sendmsg(sock, msg, flags)


@cdef('int zmq_recvmsg (void *s, zmq_msg_t *msg, int flags);')
def recvmsg(sock, msg, flags):
    return Z.zmq_recvmsg(sock, msg, flags)


ffi.cdef('struct iovec;')
ffi.cdef('int zmq_sendiov (void *s, struct iovec *iov, size_t count, int flags);')
ffi.cdef('int zmq_recviov (void *s, struct iovec *iov, size_t *count, int flags);')


# TODO:mp Windoze
ffi.cdef('''
typedef struct
{
    void *socket;
    int fd;
    short events;
    short revents;
} zmq_pollitem_t;
''')


def pollitem(socket=None, fd=0, events=0, revents=0):
    """
    Helper to create a pollitem object for zmq.poll/zpoller.poller.

    Must set either socket or fd, if socket is set, fd is ignored.
    """
    return ffi.new('zmq_pollitem_t*', 
                   dict(socket=socket, fd=fd,
                        events=events, revents=revents))


@cdef('int zmq_poll (zmq_pollitem_t *items, int nitems, long timeout);')
def poll(items, nitem, timeout):
    return Z.zmq_poll(items, nitem, timeout)


@cdef('int zmq_proxy (void *frontend, void *backend, void *capture);')
def proxy(frontend, backend, capture):
    return Z.zmq_proxy(frontend, backend, capture)


@cdef('char *zmq_z85_encode (char *dest, uint8_t *data, size_t size);')
def z85_encode(dest, data, size):
    return Z.zmq_z85_encode(dest, data, size)


@cdef('uint8_t *zmq_z85_decode (uint8_t *dest, char *string);')
def z86_decode(dest, string):
    return Z.zmq_z85_decode(dest, string)
