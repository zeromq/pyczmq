from pyczmq._cffi import C, ffi, ptop, cdef

cdef('typedef struct _zcert_t zcert_t;')


@cdef('void zcert_destroy (zcert_t **self_p);')
def destroy(cert):
    """Destroy a certificate in memory
    """
    C.zcert_destroy(ptop('zcert_t', cert))


@cdef('zcert_t * zcert_new (void);')
def new():
    """Create and initialize a new certificate in memory
    """
    return ffi.gc(C.zcert_new(), destroy)


@cdef('zcert_t * zcert_new_from (char *public_key, char *secret_key);')
def new_from(public_key, secret_key):
    """Constructor, accepts public/secret key pair from caller
    """
    return ffi.gc(C.zcert_new_from(public_key, secret_key), destroy)


@cdef('char * zcert_public_key (zcert_t *self);')
def public_key(cert):
    """Return public part of key pair as 32-byte binary string
    """
    return C.zcert_public_key(cert)


@cdef('char * zcert_secret_key (zcert_t *self);')
def secret_key(cert):
    """Return secret part of key pair as 32-byte binary string
    """
    return C.zcert_secret_key(cert)


@cdef('char * zcert_public_txt (zcert_t *self);')
def public_txt(cert):
    """
    Return public part of key pair as Z85 armored string
    """
    return ffi.string(C.zcert_public_txt(cert))


@cdef('char * zcert_secret_txt (zcert_t *self);')
def secret_txt(cert):
    """
    Return secret part of key pair as Z85 armored string
    """
    return ffi.string(C.zcert_secret_txt(cert))


@cdef('void zcert_set_meta (zcert_t *self, char *name, char *format, ...);',
      nullable=True)
def set_meta(cert, name, value):
    """
    Set certificate metadata from formatted string.
    """
    return C.zcert_set_meta(cert, name, value)


@cdef('char * zcert_meta (zcert_t *self, char *name);')
def meta(cert, name):
    """
    Get metadata value from certificate; if the metadata value doesn
    exist, returns NULL.
    """
    return ffi.string(C.zcert_meta(cert, name))


@cdef('zcert_t * zcert_load (char *fmt, ...);')
def load(filename):
    """
    Load certificate from file (constructor) The filename is treated
    as a printf format specifier.
    """
    return C.zcert_load(filename)


@cdef('int zcert_save (zcert_t *self, char *fmt, ...);')
def save(cert, filename):
    """
    Save full certificate (public + secret) to file for persistent
    storage This creates one public file and one secret file (filename
    + "_secret").  The filename is treated as a printf format
    specifier.
    """
    return C.zcert_save(cert, filename)


@cdef('int zcert_save_public (zcert_t *self, char *filename, ...);')
def save_public(cert, filename):
    """
    Save public certificate only to file for persistent storage
    The filename is treated as a printf format specifier.
    """
    return C.zcert_save_public(cert, filename)


@cdef('void zcert_apply (zcert_t *self, void *zocket);')
def apply(cert, zocket):
    """
    Apply certificate to socket, i.e. use for CURVE security on socket.
    If certificate was loaded from public file, the secret key will be
    undefined, and this certificate will not work successfully.
    """
    C.zcert_apply(cert, zocket)


@cdef('zcert_t * zcert_dup (zcert_t *self);')
def dup(cert):
    """Return copy of certificate
    """
    return C.zcert_dup(cert)


@cdef('bool zcert_eq (zcert_t *self, zcert_t *compare);')
def eq(cert, compare):
    """Return true if two certificates have the same keys
    """
    return C.zcert_eq(cert, compare)

