from pyczmq._cffi import C, ffi

ffi.cdef('''
/*  =========================================================================
    zpoller - trivial socket poller class

    -------------------------------------------------------------------------
    Copyright (c) 1991-2013 iMatix Corporation <www.imatix.com>
    Copyright other contributors as noted in the AUTHORS file.

    This file is part of CZMQ, the high-level C binding for 0MQ:
    http://czmq.zeromq.org.

    This is free software; you can redistribute it and/or modify it under the
    terms of the GNU Lesser General Public License as published by the Free
    Software Foundation; either version 3 of the License, or (at your option)
    any later version.

    This software is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABIL-
    ITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
    Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    =========================================================================
*/

//  Opaque class structure
typedef struct _zpoller_t zpoller_t;

//  @interface
//  Create new poller
 zpoller_t *
    zpoller_new (void *reader, ...);

//  Destroy a poller
 void
    zpoller_destroy (zpoller_t **self_p);

//  Poll the registered readers for I/O, return first socket that has input.
//  This means the order that sockets are defined in the poll list affects
//  their priority. If you need a balanced poll, use the low level zmq_poll
//  method directly.
 void *
    zpoller_wait (zpoller_t *self, int timeout);

//  Return true if the last zpoller_wait () call ended because the timeout
//  expired, without any error.
 bool
    zpoller_expired (zpoller_t *self);

//  Return true if the last zpoller_wait () call ended because the process
//  was interrupted, or the parent context was destroyed.
 bool
    zpoller_terminated (zpoller_t *self);

//  Self test of this class
 int
    zpoller_test (bool verbose);
''')

def new(*readers):
    poller = C.zpoller_new(*readers)
    def destroy(c):
        C.zpoller_destroy(ptop('zpoller_t', c))
    return ffi.gc(poller, destroy)

wait = C.zpoller_wait
expired = C.zpoller_expired
terminated = C.zpoller_terminated
