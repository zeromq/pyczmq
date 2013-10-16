from pyczmq._cffi import C, ffi, cdef, ptop


CURVE_ALLOW_ANY = "*"


cdef('typedef struct _zauth_t zauth_t;')


@cdef('void zauth_destroy (zauth_t **self_p);')
def destroy(auth):
    """ Destructor """
    C.zauth_destroy(ptop('zauth_t', auth))


@cdef('zauth_t * zauth_new (zctx_t *ctx);')
def new(ctx):
    """
    Install authentication for the specified context. Returns a new
    zauth object that you can use to configure authentication. Note
    that until you add policies, all incoming NULL connections are
    allowed (classic ZeroMQ behaviour), and all PLAIN and CURVE
    connections are denied. If there was an error during
    initialization, returns NULL.
    """
    return ffi.gc(C.zauth_new(ctx), destroy)


@cdef('void zauth_allow (zauth_t *self, char *address);')
def allow(auth, addr):
    """
    Allow (whitelist) a single IP address. For NULL, all clients from
    this address will be accepted. For PLAIN and CURVE, they will be
    allowed to continue with authentication. You can call this method
    multiple times to whitelist multiple IP addresses. If you
    whitelist a single address, any non-whitelisted addresses are
    treated as blacklisted.
    """
    return C.zauth_allow(auth, addr)


@cdef('void zauth_deny (zauth_t *self, char *address);')
def deny(auth, addr):
    """
    Deny (blacklist) a single IP address. For all security mechanisms,
    this rejects the connection without any further
    authentication. Use either a whitelist, or a blacklist, not not
    both. If you define both a whitelist and a blacklist, only the
    whitelist takes effect.
    """
    return C.zauth_deny(auth, addr)


@cdef('void zauth_configure_plain (zauth_t *self,'
      ' char *domain, char *filename, ...);')
def configure_plain(auth, domain, filename):
    """
    Configure PLAIN authentication for a given domain. PLAIN
    authentication uses a plain-text password file. The filename is
    treated as a printf format. To cover all domains, use "*". You can
    modify the password file at any time; it is reloaded
    automatically.
    """
    return C.zauth_configure_plain(auth, domain, filename)


@cdef('void zauth_configure_curve (zauth_t *self,'
      ' char *domain, char *location, ...);')
def configure_curve(auth, domain, location):
    """
    Configure CURVE authentication for a given domain. CURVE
    authentication uses a directory that holds all public client
    certificates, i.e. their public keys. The certificates must be in
    zcert_save () format. The location is treated as a printf
    format. To cover all domains, use "*".  You can add and remove
    certificates in that directory at any time.  To allow all client
    keys without checking, specify CURVE_ALLOW_ANY for the location.
    """
    return C.zauth_configure_curve(auth, domain, location)


@cdef('void zauth_set_verbose (zauth_t *self, bool verbose);')
def set_verbose(auth, verbose):
    """Enable verbose tracing of commands and activity"""
    return C.zauth_set_verbose(auth, verbose)


@cdef(' int zauth_test (bool verbose);')
def test(verbose):
    """Selftest"""
    return C.zauth_test(verbose)

