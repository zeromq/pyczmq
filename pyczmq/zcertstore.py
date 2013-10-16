from pyczmq._cffi import C, ffi, ptop, cdef

cdef('typedef struct _zcertstore_t zcertstore_t;')


@cdef('void zcertstore_destroy (zcertstore_t **self_p);')
def destroy(store):
    """
    Destroy a certificate store object in memory. Does not affect anything
    stored on disk.
    """
    C.zcertstore_destroy(ptop('zcertstore_t', store))


@cdef('zcertstore_t * zcertstore_new (char *location, ...);')
def new(location):
    """
    Create a new certificate store from a disk directory, loading and
    indexing all certificates in that location. The directory itself may be
    absent, and created later, or modified at any time. The certificate store
    is automatically refreshed on any zcertstore_lookup() call. If the
    location is specified as NULL, creates a pure-memory store, which you
    can work with by inserting certificates at runtime. The location is
    treated as a printf format.
    """
    return ffi.gc(C.zcertstore_new(location), destroy)


@cdef('zcert_t * zcertstore_lookup (zcertstore_t *self, char *public_key);')
def lookup(store, key):
    """
    Look up certificate by public key, returns zcert_t object if found,
    else returns NULL. The public key is provided in Z85 text format.
    """
    return C.zcertstore_lookup(store, key)


@cdef('void zcertstore_insert (zcertstore_t *self, zcert_t **cert_p);')
def insert(store, cert):
    """
    Insert certificate into certificate store in memory. Note that this
    does not save the certificate to disk. To do that, use zcert_save()
    directly on the certificate. Takes ownership of zcert_t object.
    """
    return C.zcertstore_insert(store, ptop('zcert_t', cert))


@cdef('void zcertstore_dump (zcertstore_t *self);')
def dump(store):
    """
    Print out list of certificates in store to stdout, for debugging
    purposes.
    """
    return C.zcertstore_dump(store)
