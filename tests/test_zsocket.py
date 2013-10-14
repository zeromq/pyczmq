from pyczmq import zmq, zctx, zsocket, zstr

def test_zsocket():
    ctx = zctx.new()
    push = zsocket.new(ctx, zmq.PUSH)
    pull = zsocket.new(ctx, zmq.PULL)
    zsocket.bind(push, 'inproc://test')
    zsocket.connect(pull, 'inproc://test')
    zstr.send(push, 'foo')
    assert zstr.recv(pull) == 'foo'
    zstr.send(push, 'foo')
    zsocket.poll(pull, 1)
    assert zstr.recv_nowait(pull) == 'foo'
    ctx = zctx.destroy(ctx)
