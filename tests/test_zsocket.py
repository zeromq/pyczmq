"""
Replicates czmq test_zsocket
"""

import time
from pyczmq import zmq, zctx, zframe, zsocket, zstr


def test_zsocket():

    ctx = zctx.new()

    # Create a detached thread, let it run
    interf = "*"
    domain = "localhost"
    service = 5560

    writer = zsocket.new(ctx, zmq.PUSH)
    assert (writer)
    reader = zsocket.new(ctx, zmq.PULL)
    assert (reader)
    assert zsocket.type_str(writer) == "PUSH"
    assert zsocket.type_str(reader) == "PULL"
    rc = zsocket.bind(writer, "tcp://{}:{}".format(interf, service))
    assert rc == service

    # Check unbind
    rc = zsocket.unbind(writer, "tcp://{}:{}".format(interf, service))
    assert rc == 0

    # In some cases and especially when running under Valgrind, doing
    # a bind immediately after an unbind causes an EADDRINUSE error.
    # Even a short sleep allows the OS to release the port for reuse.
    time.sleep(0.1)

    # Bind again
    rc = zsocket.bind(writer, "tcp://{}:{}".format(interf, service))
    assert rc == service


    rc = zsocket.connect(reader, "tcp://{}:{}".format(domain, service))
    assert rc == 0
    zstr.send(writer, "HELLO")
    message = zstr.recv(reader)
    assert message
    assert message == "HELLO"

    # Test binding to ports
    port = zsocket.bind(writer, "tcp://{}:*".format(interf))
    assert (port >= zsocket.DYNFROM and port <= zsocket.DYNTO)

    assert zsocket.poll(writer, 100) == False

    rc = zsocket.connect(reader, "txp://{}:{}".format(domain, service))
    assert rc == -1

    # Test sending frames to socket
    frame = zframe.new("ABC")
    rc = zframe.send(frame, writer, zframe.MORE)
    assert rc == 0
    frame = zframe.new("DEFG")
    rc = zframe.send(frame, writer, 0)
    assert rc == 0

    frame = zframe.recv(reader)
    assert zframe.streq(frame, "ABC")
    assert zframe.more(frame)
    zframe.destroy(frame)

    frame = zframe.recv(reader)
    assert zframe.streq(frame, "DEFG")
    assert not zframe.more(frame)
    zframe.destroy(frame)

    del writer
    del ctx
