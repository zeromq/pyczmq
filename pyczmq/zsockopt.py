from pyczmq._cffi import C as _C, ffi as _ffi

_ffi.cdef('''

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

ipv6 = _C.zsocket_ipv6
ipv4only = _C.zsocket_ipv4only
probe_router = _C.zsocket_probe_router
plain_server = _C.zsocket_plain_server
plain_username = _C.zsocket_plain_username
plain_password = _C.zsocket_plain_password
curve_server = _C.zsocket_curve_server
curve_publickey = _C.zsocket_curve_publickey
curve_secretkey = _C.zsocket_curve_secretkey
curve_serverkey = _C.zsocket_curve_serverkey
zap_domain = _C.zsocket_zap_domain
type = _C.zsocket_type
sndhwm = _C.zsocket_sndhwm
rcvhwm = _C.zsocket_rcvhwm
affinity = _C.zsocket_affinity
identity = _C.zsocket_identity
rate = _C.zsocket_rate
recovery_ivl = _C.zsocket_recovery_ivl
sndbuf = _C.zsocket_sndbuf
rcvbuf = _C.zsocket_rcvbuf
linger = _C.zsocket_linger
reconnect_ivl = _C.zsocket_reconnect_ivl
reconnect_ivl_max = _C.zsocket_reconnect_ivl_max
backlog = _C.zsocket_backlog
maxmsgsize = _C.zsocket_maxmsgsize
multicast_hops = _C.zsocket_multicast_hops
rcvtimeo = _C.zsocket_rcvtimeo
sndtimeo = _C.zsocket_sndtimeo
tcp_keepalive = _C.zsocket_tcp_keepalive
tcp_keepalive_idle = _C.zsocket_tcp_keepalive_idle
tcp_keepalive_cnt = _C.zsocket_tcp_keepalive_cnt
tcp_keepalive_intvl = _C.zsocket_tcp_keepalive_intvl
tcp_accept_filter = _C.zsocket_tcp_accept_filter
rcvmore = _C.zsocket_rcvmore
fd = _C.zsocket_fd
events = _C.zsocket_events
last_endpoint = _C.zsocket_last_endpoint

set_ipv6 = _C.zsocket_set_ipv6
set_immediate = _C.zsocket_set_immediate
set_router_raw = _C.zsocket_set_router_raw
set_ipv4only =_C.zsocket_set_ipv4only
set_delay_attach_on_connect = _C.zsocket_set_delay_attach_on_connect
set_router_mandatory = _C.zsocket_set_router_mandatory
set_req_relaxed = _C.zsocket_set_req_relaxed
set_req_correlate = _C.zsocket_set_req_correlate
set_conflate = _C.zsocket_set_conflate
set_plain_server = _C.zsocket_set_plain_server
set_plain_username = _C.zsocket_set_plain_username
set_plain_password = _C.zsocket_set_plain_password
set_curve_server = _C.zsocket_set_curve_server
set_curve_publickey = _C.zsocket_set_curve_publickey
set_curve_publickey_bin = _C.zsocket_set_curve_publickey_bin
set_curve_secret = _C.zsocket_set_curve_secretkey
set_curve_secretkey_bin = _C.zsocket_set_curve_secretkey_bin
set_curve_serverkey = _C.zsocket_set_curve_serverkey
set_curve_serverkey_bin = _C.zsocket_set_curve_serverkey_bin
set_zap_domain = _C.zsocket_set_zap_domain
set_sndhwm = _C.zsocket_set_sndhwm
set_rcvhwm = _C.zsocket_set_rcvhwm
set_affinity = _C.zsocket_set_affinity
set_subscribe = _C.zsocket_set_subscribe
set_unsubscribe = _C.zsocket_set_unsubscribe
set_identity = _C.zsocket_set_identity
set_rate = _C.zsocket_set_rate
set_recovery_ivl = _C.zsocket_set_recovery_ivl
set_sndbuf = _C.zsocket_set_sndbuf
set_rcvbuf = _C.zsocket_set_rcvbuf
set_linger = _C.zsocket_set_linger
set_reconnect_ivl = _C.zsocket_set_reconnect_ivl
set_reconnect_ivl_max = _C.zsocket_set_reconnect_ivl_max
set_backlog = _C.zsocket_set_backlog
set_maxmsgsize = _C.zsocket_set_maxmsgsize
set_multicast_hops = _C.zsocket_set_multicast_hops
set_rcvtimeo = _C.zsocket_set_rcvtimeo
set_sndtimeo = _C.zsocket_set_sndtimeo
set_xpub_verbose = _C.zsocket_set_xpub_verbose
set_tcp_keepalive = _C.zsocket_set_tcp_keepalive
set_tcp_keepalive_idle = _C.zsocket_set_tcp_keepalive_idle
set_tcp_keepalive_cnt = _C.zsocket_set_tcp_keepalive_cnt
set_tcp_keepalive_intvl = _C.zsocket_set_tcp_keepalive_intvl
set_tcp_accept_filter = _C.zsocket_set_tcp_accept_filter
set_hwm = _C.zsocket_set_hwm
