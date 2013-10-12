
from pyczmq import zmq, zctx, zsocket, zmsg, zframe


def test_zmsg():
    m = zmsg.new()
    foo = zframe.new('foo')
    zmsg.push(m, foo)
    assert zmsg.first(m) == foo
    bar = zframe.new('bar')
    zmsg.push(m, bar)
    assert zmsg.first(m) == bar
    assert zmsg.last(m) == foo
    zmsg.append(m, zframe.new('ding'))

    # dup and mutate the buffer view
    d = zframe.dup(zmsg.last(m))
    assert zframe.data(d)[:] == 'ding'
    zframe.data(d)[1] = 'o'
    assert zframe.data(d)[:] == 'dong'
    assert zframe.size(d) == 4
    zmsg.append(m, d)

    ctx = zctx.new()
    p = zsocket.new(ctx, zmq.PUB)
    u = zsocket.new(ctx, zmq.SUB)
    zsocket.set_subscribe(u, '')
    zsocket.bind(p, 'inproc://qer')
    zsocket.connect(u, 'inproc://qer')
    zmsg.send(m, p)
    zsocket.poll(u, 1)
    n = zmsg.recv(u)
    assert zmsg.size(n) == 4
    assert zframe.data(zmsg.next(n))[:] == 'bar'
    assert zframe.data(zmsg.next(n))[:] == 'foo'
    assert zframe.data(zmsg.next(n))[:] == 'ding'
    assert zframe.data(zmsg.next(n))[:] == 'dong'
    assert zmsg.next(n) is None
    zmsg.destroy(n)
