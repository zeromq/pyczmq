from pyczmq._cffi import C, ffi

ffi.cdef('''
/*  =========================================================================
    zbeacon - LAN service announcement and discovery
    
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
typedef struct _zbeacon_t zbeacon_t;

//  @interface
//  Create a new beacon on a certain UDP port
 zbeacon_t *
    zbeacon_new (int port_nbr);
    
//  Destroy a beacon
 void
    zbeacon_destroy (zbeacon_t **self_p);

//  Return our own IP address as printable string
 char *
    zbeacon_hostname (zbeacon_t *self);

//  Set broadcast interval in milliseconds (default is 1000 msec)
 void
    zbeacon_set_interval (zbeacon_t *self, int interval);

//  Filter out any beacon that looks exactly like ours
 void
    zbeacon_noecho (zbeacon_t *self);

//  Start broadcasting beacon to peers at the specified interval
 void
    zbeacon_publish (zbeacon_t *self, char *transmit, size_t size);
    
//  Stop broadcasting beacons
 void
    zbeacon_silence (zbeacon_t *self);

//  Start listening to other peers; zero-sized filter means get everything
 void
    zbeacon_subscribe (zbeacon_t *self, char *filter, size_t size);

//  Stop listening to other peers
 void
    zbeacon_unsubscribe (zbeacon_t *self);

//  Get beacon ZeroMQ socket, for polling or receiving messages
 void *
    zbeacon_socket (zbeacon_t *self);

//  Self test of this class
 void
    zbeacon_test (bool verbose);
''')

def new(port):
    beacon = C.zbeacon_new(port)
    def destroy(c):
        # pointer to pointer dance
        ptop = ffi.new('zbeacon_t*[1]')
        ptop[0] = c
        C.zbeacon_destroy(ptop)
    return ffi.gc(beacon, destroy)

hostname = C.zbeacon_hostname
interval = C.zbeacon_set_interval
noecho = C.zbeacon_noecho
publish = C.zbeacon_publish
silence = C.zbeacon_silence
subscribe = C.zbeacon_subscribe
unsubscribe = C.zbeacon_unsubscribe
socket = C.zbeacon_socket
test = C.zbeacon_test
