from pyczmq import zctx, zsocket, zstr


def test_zsocket():
    zsocket.test(True)
    ctx = zctx.new()
    push = zsocket.new(ctx, zsocket.PUSH)
    pull = zsocket.new(ctx, zsocket.PULL)
    zsocket.bind(push, 'inproc://test')
    zsocket.connect(pull, 'inproc://test')
    zstr.send(push, 'foo')
    assert zstr.recv_str(pull) == 'foo'
    del ctx

