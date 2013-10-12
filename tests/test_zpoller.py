from pyczmq import zmq, zctx, zsocket, zstr, zpoller


def test_zpoller():

    ctx = zctx.new()
    p = zsocket.new(ctx, zmq.PUB)
    zsocket.bind(p, 'inproc://sdf')

    s = zsocket.new(ctx, zmq.SUB)
    zsocket.set_subscribe(s, '')
    zsocket.connect(s, 'inproc://sdf')

    s2 = zsocket.new(ctx, zmq.SUB)
    zsocket.set_subscribe(s2, '')
    zsocket.connect(s2, 'inproc://sdf')

    zstr.send(p, 'foo')

    z = zpoller.new(s)
    # seg faults :(
    # x = zpoller.wait(z, -1)
