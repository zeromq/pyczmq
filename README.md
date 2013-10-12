Python CFFI wrapper around the czmq zeromq bindings.

http://czmq.zeromq.org/

The documentation for this binding can be found at readthedocs:

http://pyczmq.readthedocs.org/

This is still a work in progress, not all of the API is fully
wrapped yet.

Most of the core context, socket, socket option, polling, beacon,
auth, and cert functions are provided.

Some functions will probably not be wrapped, notably those that
provide duplicate functionality to built-in python type or libraries
like zlist, zhash, zsys, zclock, zdir, etc.

CZMQ functions are exposed via the cffi library's ABI access mode.  No
compiler is required to use it.  The czmq library is accessed with
dlopen and a set of parsed function declarations.

All CZMQ functions can be accessed directly via the low-level cffi
binding, ie:

  - pyczmq.C.zctx_new

  - pyczmq.C.zsocket_bind

  - pyczmq.C.zstr_send

  - etc...

Functions also have aliases in a module level namespace interface, so:

  - pyczmq.C.zctx_new is pyczmq.zctx.new (with caveat, see below)

  - pyczmq.C.zsocket_bind is pyczmq.zsocket.bind

  - pyczmq.C.zstr_send is pyczmq.zstr.send 

  - etc...

For example a simple PUSH/PULL socket pipeline::

    ctx = zctx.new()
    push = zsocket.new(ctx, zsocket.PUSH)
    pull = zsocket.new(ctx, zsocket.PULL)
    zsocket.bind(push, 'inproc://test')
    zsocket.connect(pull, 'inproc://test')
    zstr.send(push, 'foo')
    assert zstr.recv(pull) == 'foo'
    zstr.send(push, 'foo')
    zsocket.poll(pull, 1)
    assert zstr.recv_nowait(pull) == 'foo'

Some of the 'new' functions in the module namespaces (like
pyczmq.zctx.new) are wrappers that plug into Python's garbage
collector, so you typically never need to explicitly destroy objects
if you use the namespace interface.  Therefore, pyczmq.zctx.new isn't
*really* pyczmq.C.zmq_new, but the effect is exactly the same.  If you
use the "raw" C binding interface pyczmq.C.zctx_new, however, you must
explicitly garbage collect your own resources by calling the
coresponding destroy method (pyczmq.C.zctx_destroy, etc.).

Some 'new' functions do not do this wrapping behavior, because they
are meant to be destroyed by czmq.  zmsg objects for example are
destroyed by zmsg_send, and zframe objects have their ownership taken
over by various functions in zmsg and are destroyed when the msg is
sent and destroyed.  If you create these objects and don't in turn
call the functions that destroy them, you must explicitly destroy them
yourself with zmsg.destroy or zframe.destroy.

Like what you see?  If you feel like leaving me or other open source
developers a tip for our work, please visit gittip:

https://www.gittip.com/michelp/