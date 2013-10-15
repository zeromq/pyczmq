"""
Replicates czmq test_zpoller
"""

from pyczmq import zmq, zctx, zpoller, zsocket, zstr


def test_zpoller(verbose=False):

    ctx = zctx.new()

    # Create a few sockets
    vent = zsocket.new(ctx, zmq.PUSH);
    rc = zsocket.bind(vent, "tcp://*:9000")
    assert rc != -1, "vent bind error"
    sink = zsocket.new(ctx, zmq.PULL)
    rc = zsocket.connect(sink, "tcp://localhost:9000");
    assert rc != -1, "sink connect error"
    bowl = zsocket.new(ctx, zmq.PULL)
    dish = zsocket.new(ctx, zmq.PULL)

    # Set-up poller
    poller = zpoller.new(bowl, sink, dish)
    assert poller, "poller create error"

    zstr.send(vent, "Hello, World")

    # We expect a message only on the sink
    which = zpoller.wait(poller, 1000)

    assert which == sink, "expected message on sink only"
    assert not zpoller.expired(poller), "unexpected poll timer exipiry"
    assert not zpoller.terminated(poller), "unexpected poller termination (interrupted)"

    message = zstr.recv(which)
    assert message == "Hello, World", "unexpected message recevied"

    # Destroy poller and context
    poller = zpoller.destroy(poller)
    ctx = zctx.destroy(ctx)
