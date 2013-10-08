from pyczmq._cffi import C, ffi

ffi.cdef('''
/*  =========================================================================
    zcert - work with CURVE security certificates

    -------------------------------------------------------------------------
    Copyright (c) 1991-2013 iMatix Corporation <www.imatix.com>
    Copyright other contributors as noted in the AUTHORS file.

    This file is part of CZMQ, the high-level C binding for 0MQ:
    http://czmq.zeromq.org.

    This is free software; you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License as published by the
    Free Software Foundation; either version 3 of the License, or (at your
    option) any later version.

    This software is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABIL-
    ITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
    Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    =========================================================================
*/

//  Opaque class structure
typedef struct _zcert_t zcert_t;

//  Create and initialize a new certificate in memory
 zcert_t *
    zcert_new (void);

//  Constructor, accepts public/secret key pair from caller
 zcert_t *
    zcert_new_from (char *public_key, char *secret_key);

//  Destroy a certificate in memory
 void
    zcert_destroy (zcert_t **self_p);

//  Return public part of key pair as 32-byte binary string
 char *
    zcert_public_key (zcert_t *self);

//  Return secret part of key pair as 32-byte binary string
 char *
    zcert_secret_key (zcert_t *self);

//  Return public part of key pair as Z85 armored string
 char *
    zcert_public_txt (zcert_t *self);

//  Return secret part of key pair as Z85 armored string
 char *
    zcert_secret_txt (zcert_t *self);

//  Set certificate metadata from formatted string.
 void
    zcert_set_meta (zcert_t *self, char *name, char *format, ...);

//  Get metadata value from certificate; if the metadata value doesn't 
//  exist, returns NULL.
 char *
    zcert_meta (zcert_t *self, char *name);

//  Load certificate from file (constructor)
//  The filename is treated as a printf format specifier.
 zcert_t *
    zcert_load (char *filename, ...);

//  Save full certificate (public + secret) to file for persistent storage
//  This creates one public file and one secret file (filename + "_secret").
//  The filename is treated as a printf format specifier.
 int
    zcert_save (zcert_t *self, char *filename, ...);

//  Save public certificate only to file for persistent storage
//  The filename is treated as a printf format specifier.
 int
    zcert_save_public (zcert_t *self, char *filename, ...);

//  Apply certificate to socket, i.e. use for CURVE security on socket.
//  If certificate was loaded from public file, the secret key will be
//  undefined, and this certificate will not work successfully.
 void
    zcert_apply (zcert_t *self, void *zocket);

//  Return copy of certificate
 zcert_t *
    zcert_dup (zcert_t *self);

//  Return true if two certificates have the same keys
 bool
    zcert_eq (zcert_t *self, zcert_t *compare);

//  Dump certificate contents to stderr for debugging
 void
    zcert_dump (zcert_t *self);

//  Self test of this class
 int
    zcert_test (bool verbose);
''')


def new():
    cert = C.zcert_new()
    def destroy(c):
        # pointer to pointer dance
        ptop = ffi.new('zcert_t*[1]')
        ptop[0] = c
        C.zcert_destroy(ptop)
    return ffi.gc(cert, destroy)


def new_from(public_key, secret_key):
    cert = C.zcert_new_from(public_key, secret_key)
    def destroy(c):
        # pointer to pointer dance
        ptop = ffi.new('zcert_t*[1]')
        ptop[0] = c
        C.zcert_destroy(ptop)
    return ffi.gc(cert, destroy)


# why don't these work? -mp
# public_key = C.zcert_public_key
# secret_key = C.zcert_secret_key
public_txt = C.zcert_public_txt
secret_txt = C.zcert_secret_txt
set_meta = C.zcert_set_meta
meta = C.zcert_meta
load = C.zcert_load
save = C.zcert_save
save_public = C.zcert_save_public
apply = C.zcert_apply
dup = C.zcert_dup
eq = C.zcert_eq
dump = C.zcert_dump
test = C.zcert_test
