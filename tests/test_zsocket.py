from pyczmq import zctx, zsocket, zstr

def test_zsocket():
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
