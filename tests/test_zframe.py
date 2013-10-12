
"""
Replicates czmq test_zframe
"""

from pyczmq import zmq, zctx, zframe, zsocket


def test_zframe():
    ctx = zctx.new()
    test_endpoint = 'inproc://zframe.test'
    output_s = zsocket.new(ctx, zmq.PAIR)
    zsocket.bind(output_s, test_endpoint)
    input_s = zsocket.new(ctx, zmq.PAIR)
    zsocket.connect(input_s, test_endpoint)

    # Send five different frames, test ZFRAME_MORE
    for i in range(0, 5):
        frame = zframe.new("Hello")
        rc = zframe.send(frame, output_s, zframe.MORE)
        assert(rc == 0)

    # Send same frame five times, test ZFRAME_REUSE
    frame = zframe.new("Hello")
    for i in range(0, 5):
        rc = zframe.send(frame, output_s, zframe.MORE + zframe.REUSE)
        assert(rc == 0)
    assert(frame)

    copy = zframe.dup(frame)
    assert (zframe.eq(frame, copy))

    zframe.reset(frame, "")
    assert (not zframe.eq(frame, copy))
    assert (zframe.size(copy) == 5)
    zframe.destroy(frame)
    zframe.destroy(copy)

    # Test zframe_new_empty
    frame = zframe.new_empty()
    assert(frame)
    assert(zframe.size(frame) == 0)
    zframe.destroy(frame)

    # Send END frame
    frame = zframe.new("NOT")
    zframe.reset(frame, "END")
    hex_string = zframe.strhex(frame)
    assert(hex_string == "454E44")

    frame_bytes = zframe.data(frame)
    assert frame_bytes == "END"


    string = zframe.strdup(frame)
    assert(string == "END")
    rc = zframe.send(frame, output_s, 0)
    assert(rc == 0)

    # Read and count until we receive END
    frame_nbr = 0
    while True:
        frame = zframe.recv(input_s)
        frame_nbr += 1
        if zframe.streq(frame, "END"):
            zframe.destroy(frame)
            break
        else:
            assert(zframe.size(frame) == 5)
            assert zframe.data(frame) == "Hello"
        assert(zframe.more(frame))
        zframe.set_more(frame, 0)
        assert(zframe.more(frame) == 0)
        zframe.destroy(frame)
    assert(frame_nbr == 11)
    frame = zframe.recv_nowait(input_s)
    assert(frame is None)
