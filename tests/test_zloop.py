from pyczmq import ffi, zmq, zctx, zsocket, zstr, zloop

def test_zloop():
    ctx = zctx.new()
    p = zsocket.new(ctx, zmq.PUSH)
    u = zsocket.new(ctx, zmq.PULL)
    zsocket.bind(p, 'inproc://lkj')
    zsocket.connect(u, 'inproc://lkj')

    l = zloop.new()
    item = zmq.pollitem(socket=u, events=zmq.POLLIN)

    @ffi.callback('zloop_fn')
    def handler(loop, item, arg):
        assert zstr.recv(item.socket) == 'foo'
        assert ffi.from_handle(arg) == 3
        return -1

    zloop.poller(l, item, handler, 3)
    zstr.send(p, 'foo')
    zloop.start(l)
