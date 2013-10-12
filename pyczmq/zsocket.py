from pyczmq._cffi import C, ffi, cdef

__doc__ = """
The zsocket class provides helper functions for 0MQ sockets. It
doesn't wrap the 0MQ socket type, to avoid breaking all libzmq
socket-related calls.
"""

@cdef('void zsocket_destroy (zctx_t *self, void *socket);')
def destroy(ctx, socket):
    """Destroy a socket within our CZMQ context.

    'pyczmq.zsocket.new' automatically registers this destructor with
    the garbage collector, so this is normally not necessary to use,
    unless you need to destroy sockets created by some other means
    (like a call directly to 'pyczmq.C.zsocket_new')
    """
    return C.zsocket_destroy(ctx, socket)


@cdef('void * zsocket_new (zctx_t *self, int type);')
def new(ctx, typ):
    """
    Create a new socket within our CZMQ context, replaces zmq_socket.
    Use this to get automatic management of the socket at shutdown.
    Note: SUB sockets do not automatically subscribe to everything;
    you must set filters explicitly.
    """
    return ffi.gc(C.zsocket_new(ctx, typ), lambda s: destroy(ctx, s))


@cdef('int zsocket_bind (void *socket, const char *format, ...);')
def bind(sock, fmt):
    """
    Bind a socket to a formatted endpoint. If the port is specified as
    '*', binds to any free port from ZSOCKET_DYNFROM to ZSOCKET_DYNTO
    and returns the actual port number used. Otherwise asserts that
    the bind succeeded with the specified port number. Always returns
    the port number if successful.
    """
    return C.zsocket_bind(sock, fmt)


@cdef('int zsocket_unbind (void *socket, const char *format, ...);')
def unbind(sock, fmt):
    """
    Unbind a socket from a formatted endpoint.  Returns 0 if OK, -1 if
    the endpoint was invalid or the function isn't supported.
    """
    return C.zsocket_unbind(sock, fmt)


@cdef('int zsocket_connect (void *socket, const char *format, ...);')
def connect(sock, fmt):
    """
    Connect a socket to a formatted endpoint Returns 0 if OK, -1 if
    the endpoint was invalid.
    """
    return C.zsocket_connect(sock, fmt)


@cdef('int zsocket_disconnect (void *socket, const char *format, ...);')
def disconnect(sock, fmt):
    """
    Disonnect a socket from a formatted endpoint Returns 0 if OK, -1
    if the endpoint was invalid or the function isn't supported.
    """
    return C.zsocket_disconnect(sock, fmt)


@cdef('bool zsocket_poll (void *socket, int msecs);')
def poll(sock, msecs):
    """
    Poll for input events on the socket. Returns TRUE if there is input
    ready on the socket, else FALSE.
    """
    return C.zsocket_poll(sock, msecs)


@cdef('char * zsocket_type_str (void *socket);')
def type_str(sock):
    """Returns socket type as printable constant string"""
    return C.zsocket_type_str(sock)

cdef('''

/*  =========================================================================
    zsockopt - get/set 0MQ socket options

            ****************************************************
            *   GENERATED SOURCE CODE, DO NOT EDIT!!           *
            *   TO CHANGE THIS, EDIT scripts/sockopts.gsl      *
            *   AND RUN ./generate in models/.                 *
            ****************************************************
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

 int zsocket_ipv6 (void *zocket);
 int zsocket_ipv4only (void *zocket);
 int zsocket_probe_router (void *zocket);
 int zsocket_plain_server (void *zocket);
 char * zsocket_plain_username (void *zocket);
 char * zsocket_plain_password (void *zocket);
 int zsocket_curve_server (void *zocket);
 char * zsocket_curve_publickey (void *zocket);
 char * zsocket_curve_secretkey (void *zocket);
 char * zsocket_curve_serverkey (void *zocket);
 char * zsocket_zap_domain (void *zocket);
 int zsocket_type (void *zocket);
 int zsocket_sndhwm (void *zocket);
 int zsocket_rcvhwm (void *zocket);
 int zsocket_affinity (void *zocket);
 char * zsocket_identity (void *zocket);
 int zsocket_rate (void *zocket);
 int zsocket_recovery_ivl (void *zocket);
 int zsocket_sndbuf (void *zocket);
 int zsocket_rcvbuf (void *zocket);
 int zsocket_linger (void *zocket);
 int zsocket_reconnect_ivl (void *zocket);
 int zsocket_reconnect_ivl_max (void *zocket);
 int zsocket_backlog (void *zocket);
 int zsocket_maxmsgsize (void *zocket);
 int zsocket_multicast_hops (void *zocket);
 int zsocket_rcvtimeo (void *zocket);
 int zsocket_sndtimeo (void *zocket);
 int zsocket_tcp_keepalive (void *zocket);
 int zsocket_tcp_keepalive_idle (void *zocket);
 int zsocket_tcp_keepalive_cnt (void *zocket);
 int zsocket_tcp_keepalive_intvl (void *zocket);
 char * zsocket_tcp_accept_filter (void *zocket);
 int zsocket_rcvmore (void *zocket);
 int zsocket_fd (void *zocket);
 int zsocket_events (void *zocket);
 char * zsocket_last_endpoint (void *zocket);

//  Set socket options
 void zsocket_set_ipv6 (void *zocket, int ipv6);
 void zsocket_set_immediate (void *zocket, int immediate);
 void zsocket_set_router_raw (void *zocket, int router_raw);
 void zsocket_set_ipv4only (void *zocket, int ipv4only);
 void zsocket_set_delay_attach_on_connect (void *zocket, int delay_attach_on_connect);
 void zsocket_set_router_mandatory (void *zocket, int router_mandatory);
 void zsocket_set_req_relaxed (void *zocket, int req_relaxed);
 void zsocket_set_req_correlate (void *zocket, int req_correlate);
 void zsocket_set_conflate (void *zocket, int conflate);
 void zsocket_set_plain_server (void *zocket, int plain_server);
 void zsocket_set_plain_username (void *zocket, const char * plain_username);
 void zsocket_set_plain_password (void *zocket, const char * plain_password);
 void zsocket_set_curve_server (void *zocket, int curve_server);
 void zsocket_set_curve_publickey (void *zocket, const char * curve_publickey);
 void zsocket_set_curve_publickey_bin (void *zocket, const char *curve_publickey);
 void zsocket_set_curve_secretkey (void *zocket, const char * curve_secretkey);
 void zsocket_set_curve_secretkey_bin (void *zocket, const char *curve_secretkey);
 void zsocket_set_curve_serverkey (void *zocket, const char * curve_serverkey);
 void zsocket_set_curve_serverkey_bin (void *zocket, const char *curve_serverkey);
 void zsocket_set_zap_domain (void *zocket, const char * zap_domain);
 void zsocket_set_sndhwm (void *zocket, int sndhwm);
 void zsocket_set_rcvhwm (void *zocket, int rcvhwm);
 void zsocket_set_affinity (void *zocket, int affinity);
 void zsocket_set_subscribe (void *zocket, const char * subscribe);
 void zsocket_set_unsubscribe (void *zocket, const char * unsubscribe);
 void zsocket_set_identity (void *zocket, const char * identity);
 void zsocket_set_rate (void *zocket, int rate);
 void zsocket_set_recovery_ivl (void *zocket, int recovery_ivl);
 void zsocket_set_sndbuf (void *zocket, int sndbuf);
 void zsocket_set_rcvbuf (void *zocket, int rcvbuf);
 void zsocket_set_linger (void *zocket, int linger);
 void zsocket_set_reconnect_ivl (void *zocket, int reconnect_ivl);
 void zsocket_set_reconnect_ivl_max (void *zocket, int reconnect_ivl_max);
 void zsocket_set_backlog (void *zocket, int backlog);
 void zsocket_set_maxmsgsize (void *zocket, int maxmsgsize);
 void zsocket_set_multicast_hops (void *zocket, int multicast_hops);
 void zsocket_set_rcvtimeo (void *zocket, int rcvtimeo);
 void zsocket_set_sndtimeo (void *zocket, int sndtimeo);
 void zsocket_set_xpub_verbose (void *zocket, int xpub_verbose);
 void zsocket_set_tcp_keepalive (void *zocket, int tcp_keepalive);
 void zsocket_set_tcp_keepalive_idle (void *zocket, int tcp_keepalive_idle);
 void zsocket_set_tcp_keepalive_cnt (void *zocket, int tcp_keepalive_cnt);
 void zsocket_set_tcp_keepalive_intvl (void *zocket, int tcp_keepalive_intvl);
 void zsocket_set_tcp_accept_filter (void *zocket, const char * tcp_accept_filter);

//  Emulation of widely-used 2.x socket options
 void zsocket_set_hwm (void *zocket, int hwm);

int zsockopt_test (bool verbose);
''')

ipv6 = C.zsocket_ipv6
ipv4only = C.zsocket_ipv4only
probe_router = C.zsocket_probe_router
plain_server = C.zsocket_plain_server
plain_username = C.zsocket_plain_username
plain_password = C.zsocket_plain_password
curve_server = C.zsocket_curve_server
curve_publickey = C.zsocket_curve_publickey
curve_secretkey = C.zsocket_curve_secretkey
curve_serverkey = C.zsocket_curve_serverkey
zap_domain = C.zsocket_zap_domain
type = C.zsocket_type
sndhwm = C.zsocket_sndhwm
rcvhwm = C.zsocket_rcvhwm
affinity = C.zsocket_affinity
identity = C.zsocket_identity
rate = C.zsocket_rate
recovery_ivl = C.zsocket_recovery_ivl
sndbuf = C.zsocket_sndbuf
rcvbuf = C.zsocket_rcvbuf
linger = C.zsocket_linger
reconnect_ivl = C.zsocket_reconnect_ivl
reconnect_ivl_max = C.zsocket_reconnect_ivl_max
backlog = C.zsocket_backlog
maxmsgsize = C.zsocket_maxmsgsize
multicast_hops = C.zsocket_multicast_hops
rcvtimeo = C.zsocket_rcvtimeo
sndtimeo = C.zsocket_sndtimeo
tcp_keepalive = C.zsocket_tcp_keepalive
tcp_keepalive_idle = C.zsocket_tcp_keepalive_idle
tcp_keepalive_cnt = C.zsocket_tcp_keepalive_cnt
tcp_keepalive_intvl = C.zsocket_tcp_keepalive_intvl
tcp_accept_filter = C.zsocket_tcp_accept_filter
rcvmore = C.zsocket_rcvmore
fd = C.zsocket_fd
events = C.zsocket_events
last_endpoint = C.zsocket_last_endpoint

set_ipv6 = C.zsocket_set_ipv6
set_immediate = C.zsocket_set_immediate
set_router_raw = C.zsocket_set_router_raw
set_ipv4only =C.zsocket_set_ipv4only
set_delay_attach_on_connect = C.zsocket_set_delay_attach_on_connect
set_router_mandatory = C.zsocket_set_router_mandatory
set_req_relaxed = C.zsocket_set_req_relaxed
set_req_correlate = C.zsocket_set_req_correlate
set_conflate = C.zsocket_set_conflate
set_plain_server = C.zsocket_set_plain_server
set_plain_username = C.zsocket_set_plain_username
set_plain_password = C.zsocket_set_plain_password
set_curve_server = C.zsocket_set_curve_server
set_curve_publickey = C.zsocket_set_curve_publickey
set_curve_publickey_bin = C.zsocket_set_curve_publickey_bin
set_curve_secret = C.zsocket_set_curve_secretkey
set_curve_secretkey_bin = C.zsocket_set_curve_secretkey_bin
set_curve_serverkey = C.zsocket_set_curve_serverkey
set_curve_serverkey_bin = C.zsocket_set_curve_serverkey_bin
set_zap_domain = C.zsocket_set_zap_domain
set_sndhwm = C.zsocket_set_sndhwm
set_rcvhwm = C.zsocket_set_rcvhwm
set_affinity = C.zsocket_set_affinity
set_subscribe = C.zsocket_set_subscribe
set_unsubscribe = C.zsocket_set_unsubscribe
set_identity = C.zsocket_set_identity
set_rate = C.zsocket_set_rate
set_recovery_ivl = C.zsocket_set_recovery_ivl
set_sndbuf = C.zsocket_set_sndbuf
set_rcvbuf = C.zsocket_set_rcvbuf
set_linger = C.zsocket_set_linger
set_reconnect_ivl = C.zsocket_set_reconnect_ivl
set_reconnect_ivl_max = C.zsocket_set_reconnect_ivl_max
set_backlog = C.zsocket_set_backlog
set_maxmsgsize = C.zsocket_set_maxmsgsize
set_multicast_hops = C.zsocket_set_multicast_hops
set_rcvtimeo = C.zsocket_set_rcvtimeo
set_sndtimeo = C.zsocket_set_sndtimeo
set_xpub_verbose = C.zsocket_set_xpub_verbose
set_tcp_keepalive = C.zsocket_set_tcp_keepalive
set_tcp_keepalive_idle = C.zsocket_set_tcp_keepalive_idle
set_tcp_keepalive_cnt = C.zsocket_set_tcp_keepalive_cnt
set_tcp_keepalive_intvl = C.zsocket_set_tcp_keepalive_intvl
set_tcp_accept_filter = C.zsocket_set_tcp_accept_filter
set_hwm = C.zsocket_set_hwm
