Python CFFI wrapper around the czmq zeromq bindings.

http://czmq.zeromq.org/

This is still a work in progress, not all of the API is fully
wrapped yet.

CZMQ functions are exposed via the cffi library's ABI access mode.  No
compiler is required to use it.  The czmq library is accessed with
dlopen and a set of parsed function declarations.

All CZMQ functions can be access one of three ways, directly via the
low-level cffi binding, ie:

   - pyczmq.C.zctx_new

   - pyczmq.C.zsocket_bind

   - pyczmq.C.zstr_send

   etc...

Functions also have aliases in module namespaces, so:

   - pyczmq.zctx.new is pyczmq.C.zctx_new

   - pyczmq.zsocket.bind is pyczmq.C.zsocket_bind

   - pyczmq.zstr.send is pyczmq.C.zstr_send

   etc...

Functionality is also encapsulated in a number of helper classes to
make the API more "object oriented".  Types included are 'Context',
'Socket', 'Loop' and 'Beacon'.
