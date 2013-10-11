from __future__ import print_function

__doc__ = """
The zframe class provides methods to send and receive single message
frames across 0MQ sockets. A frame corresponds to one zmq_msg_t. When
you read a frame from a socket, the zframe_more() method indicates if
the frame is part of an unfinished multipart message. The zframe_send
method normally destroys the frame, but with the ZFRAME_REUSE flag,
you can send the same frame many times. Frames are binary, and this
class has no special support for text data.
"""

from pyczmq._cffi import C, ffi, tostr

ffi.cdef('''
/*  =========================================================================
    zframe - working with single message frames

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
typedef struct _zframe_t zframe_t;

//  Create a new frame with optional size, and optional data
 zframe_t *
    zframe_new (const void *data, size_t size);

//  Create an empty (zero-sized) frame
 zframe_t *
    zframe_new_empty (void);

//  Destroy a frame
 void
    zframe_destroy (zframe_t **self_p);

//  Receive frame from socket, returns zframe_t object or NULL if the recv
//  was interrupted. Does a blocking recv, if you want to not block then use
//  zframe_recv_nowait().
 zframe_t *
    zframe_recv (void *socket);

//  Receive a new frame off the socket. Returns newly allocated frame, or
//  NULL if there was no input waiting, or if the read was interrupted.
 zframe_t *
    zframe_recv_nowait (void *socket);

// Send a frame to a socket, destroy frame after sending.
// Return -1 on error, 0 on success.
 int
    zframe_send (zframe_t **self_p, void *socket, int flags);

//  Return number of bytes in frame data
 size_t
    zframe_size (zframe_t *self);

//  Return address of frame data
 char *
    zframe_data (zframe_t *self);

//  Create a new frame that duplicates an existing frame
 zframe_t *
    zframe_dup (zframe_t *self);

//  Return frame data encoded as printable hex string
 char *
    zframe_strhex (zframe_t *self);

//  Return frame data copied into freshly allocated string
 char *
    zframe_strdup (zframe_t *self);

//  Return TRUE if frame body is equal to string, excluding terminator
 bool
    zframe_streq (zframe_t *self, const char *string);

//  Return frame MORE indicator (1 or 0), set when reading frame from socket
//  or by the zframe_set_more() method
 int
    zframe_more (zframe_t *self);

//  Set frame MORE indicator (1 or 0). Note this is NOT used when sending 
//  frame to socket, you have to specify flag explicitly.
 void
    zframe_set_more (zframe_t *self, int more);
    
//  Return TRUE if two frames have identical size and data
//  If either frame is NULL, equality is always false.
 bool
    zframe_eq (zframe_t *self, zframe_t *other);

//   Print contents of the frame to FILE stream.
 void
    zframe_fprint (zframe_t *self, const char *prefix, FILE *file);

//  Print contents of frame to stderr
 void
    zframe_print (zframe_t *self, const char *prefix);

//  Set new contents for frame
 void
    zframe_reset (zframe_t *self, const void *data, size_t size);

//  Self test of this class
 int
    zframe_test (bool verbose);
''')


def new(data):
    return C.zframe_new(data, len(data))

MORE = 1
REUSE = 2
DONTWAIT = 4

recv = C.zframe_recv
recv_nowait = C.zframe_recv_nowait
send = C.zframe_send
size = C.zframe_size;
data = tostr(C.zframe_data)
dup = C.zframe_dup
strhex = tostr(C.zframe_strhex)
strdup = C.zframe_strdup
streq = C.zframe_streq
more = C.zframe_more
set_more = C.zframe_set_more
eq = C.zframe_eq
fprint = C.zframe_fprint
print = C.zframe_print
reset = C.zframe_reset
test = C.zframe_test
