import pyczmq
from pyczmq import zctx, zsocket, zsockopt, zmsg, zframe, ffi

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
    assert zframe.data(zmsg.last(m)) == 'ding'

    ctx = zctx.new()
    p = zsocket.new(ctx, zsocket.PUB)
    u = zsocket.new(ctx, zsocket.SUB)
    zsockopt.set_subscribe(u, '')
    zsocket.bind(p, 'inproc://qer')
    zsocket.connect(u, 'inproc://qer')
    zmsg.send(m, p)
    zsocket.poll(u, 1)
    n = zmsg.recv(u)
    assert zmsg.size(n) == 3
    assert zframe.data(zmsg.next(n)) == 'bar'
    assert zframe.data(zmsg.next(n)) == 'foo'
    assert zframe.data(zmsg.next(n)) == 'ding'
    assert zmsg.next(n) is None
