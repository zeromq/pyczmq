from pyczmq import ffi, zmq, zctx, zsocket, zstr, zloop

def test_zloop():
    ctx = zctx.new()
    output = zsocket.new(ctx, zmq.PAIR)
    input = zsocket.new(ctx, zmq.PAIR)
    zsocket.bind(output, 'inproc://lkj')
    zsocket.connect(input, 'inproc://lkj')

    @ffi.callback('zloop_fn')
    def item_handler(loop, item, arg):
        assert zstr.recv(item.socket) == 'PING'
        assert ffi.from_handle(arg) == 3
        return -1

    @ffi.callback('zloop_fn')
    def timer_handler(loop, item, arg):
        zstr.send(arg, 'PING')
        return 0

    l = zloop.new()
    zloop.timer(l, 10, 1, timer_handler, output)
    zloop.poller(
        l, zmq.pollitem(socket=input, events=zmq.POLLIN), item_handler, 3)
    zloop.start(l)

    l = zloop.destroy(l)
