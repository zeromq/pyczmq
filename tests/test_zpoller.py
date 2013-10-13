from pyczmq import zmq, zctx, zpoller, zsocket, zstr


def test_zpoller():

    ctx = zctx.new()

    # Create a few sockets
    vent = zsocket.new(ctx, zmq.PUSH);
    rc = zsocket.bind(vent, "tcp://*:9000")
    assert rc != -1
    sink = zsocket.new(ctx, zmq.PULL)
    rc = zsocket.connect(sink, "tcp://127.0.0.1:9000");
    assert rc != -1
    bowl = zsocket.new(ctx, zmq.PULL)
    dish = zsocket.new(ctx, zmq.PULL)

    # Set-up poller
    poller = zpoller.new(bowl, sink, dish)
    assert poller

    zstr.send(vent, "Hello, World")

    # We expect a message only on the sink
    which = zpoller.wait(poller, 1000)

    assert which == sink
    assert not zpoller.expired(poller)
    assert not zpoller.terminated(poller)

    message = zstr.recv(which)
    assert message == "Hello, World"

    # There is currently something wrong with manually calling
    # delete. Probably something to do with hooking the delete
    # to ffi.gc ??
    #
    # Destroy poller and context
    #zpoller.destroy(poller)
