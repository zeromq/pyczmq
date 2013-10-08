from pyczmq import types, zsocket

def test_types():
    ctx = types.Context()
    pub = ctx.socket(zsocket.PUB)
    sub = ctx.socket(zsocket.SUB)
    sub.set_subscribe('')
    pub.bind('inproc://zoop')
    sub.connect('inproc://zoop')
    pub.send('foo')
    sub.poll(1)
    assert sub.recv() == 'foo'
