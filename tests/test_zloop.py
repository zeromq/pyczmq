from pyczmq import ffi, zctx, zsocket, zstr, zloop

def test_zloop():
    ctx = zctx.new()
    p = zsocket.new(ctx, zsocket.PUSH)
    u = zsocket.new(ctx, zsocket.PULL)
    zsocket.bind(p, 'inproc://lkj')
    zsocket.connect(u, 'inproc://lkj')

    l = zloop.new()
    item = zloop.item(socket=u, fd=0, events=zloop.POLLIN)

    @ffi.callback('zloop_fn')
    def handler(loop, item, arg):
        assert zstr.recv(item.socket) == 'foo'
        assert ffi.from_handle(arg) == 3
        return -1

    zloop.poller(l, item, handler, 3)
    zstr.send(p, 'foo')
    zloop.start(l)
