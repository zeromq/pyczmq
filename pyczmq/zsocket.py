from pyczmq._cffi import C, ffi

ffi.cdef('''
/*  =========================================================================
    zsocket - working with 0MQ sockets

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

//  Callback function for zero-copy methods
typedef void (zsocket_free_fn) (void *data, void *arg);

//  Create a new socket within our CZMQ context, replaces zmq_socket.
//  Use this to get automatic management of the socket at shutdown.
//  Note: SUB sockets do not automatically subscribe to everything; you
//  must set filters explicitly.
 void * zsocket_new (zctx_t *self, int type);

//  Destroy a socket within our CZMQ context, replaces zmq_close.
 void zsocket_destroy (zctx_t *self, void *socket);

//  Bind a socket to a formatted endpoint. If the port is specified as
//  '*', binds to any free port from ZSOCKET_DYNFROM to ZSOCKET_DYNTO
//  and returns the actual port number used. Otherwise asserts that the
//  bind succeeded with the specified port number. Always returns the
//  port number if successful.
 int zsocket_bind (void *socket, const char *format, ...);

//  Unbind a socket from a formatted endpoint.
//  Returns 0 if OK, -1 if the endpoint was invalid or the function
//  isn't supported.
 int zsocket_unbind (void *socket, const char *format, ...);

//  Connect a socket to a formatted endpoint
//  Returns 0 if OK, -1 if the endpoint was invalid.
 int zsocket_connect (void *socket, const char *format, ...);

//  Disonnect a socket from a formatted endpoint
//  Returns 0 if OK, -1 if the endpoint was invalid or the function
//  isn't supported.
 int zsocket_disconnect (void *socket, const char *format, ...);

//  Poll for input events on the socket. Returns TRUE if there is input
//  ready on the socket, else FALSE.
 bool zsocket_poll (void *socket, int msecs);

//  Returns socket type as printable constant string
 char * zsocket_type_str (void *socket);

//  Send data over a socket as a single frame
//  Returns -1 on error, 0 on success
 int zsocket_sendmem (void *socket, const void* data, size_t size, int flags);

//  Self test of this class
 int zsocket_test (bool verbose);
''')

def new(ctx, typ):
    return ffi.gc(C.zsocket_new(ctx, typ), lambda s: C.zsocket_destroy(ctx, s))

bind = C.zsocket_bind
unbind = C.zsocket_unbind
connect = C.zsocket_connect
disconnect = C.zsocket_disconnect
poll = C.zsocket_poll
type_str = C.zsocket_type_str
sendmem = C.zsocket_sendmem
test = C.zsocket_test

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
