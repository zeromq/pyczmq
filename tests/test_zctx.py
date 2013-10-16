"""
Replicates czmq test_zctx
"""

from pyczmq import ffi, zctx, zmq, zsocket

def test_zctx():

    # Create and destroy a context without using it
    ctx = zctx.new()
    assert ctx
    del ctx

    # Create a context with many busy sockets, destroy it
    ctx = zctx.new()
    assert ctx

    # call API functions
    zctx.set_iothreads(ctx, 1)
    zctx.set_linger(ctx, 5) # 5 msecs
    zctx.set_pipehwm(ctx, 500)
    zctx.set_sndhwm(ctx, 500)
    zctx.set_rcvhwm(ctx, 500)

    s1 = zsocket.new(ctx, zmq.PAIR)
    s2 = zsocket.new(ctx, zmq.PULL)  # zmq.XREQ ?
    s3 = zsocket.new(ctx, zmq.REQ)
    s4 = zsocket.new(ctx, zmq.REP)
    s5 = zsocket.new(ctx, zmq.PUB)
    s6 = zsocket.new(ctx, zmq.SUB)
    zsocket.connect(s1, "tcp://127.0.0.1:5555")
    zsocket.connect(s2, "tcp://127.0.0.1:5555")
    zsocket.connect(s3, "tcp://127.0.0.1:5555")
    zsocket.connect(s4, "tcp://127.0.0.1:5555")
    zsocket.connect(s5, "tcp://127.0.0.1:5555")
    zsocket.connect(s6, "tcp://127.0.0.1:5555")

    assert zctx.underlying(ctx);
    del ctx
