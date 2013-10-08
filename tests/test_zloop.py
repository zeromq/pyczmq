from pyczmq import zctx, zsocket, zstr, zloop

def test_zloop():
    ctx = zctx.new()
    p = zsocket.new(ctx, zsocket.PUSH)
    u = zsocket.new(ctx, zsocket.PULL)
    zsocket.bind(p, 'inproc://lkj')
    zsocket.connect(u, 'inproc://lkj')

    l = zloop.new()
    item = zloop.item(socket=u, fd=0, events=zloop.POLLIN)

    def handler(loop, item, arg):
        return 1

    zloop.poller(l, item, handler, 3)
    zstr.send(p, 'foo')
    zloop.set_verbose(l, True)
    # dying on SIGIL, wtf?
    #zloop.start(l)
