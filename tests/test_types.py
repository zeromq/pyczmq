from pyczmq import Context

def test_types():
    ctx = Context()
    pub = ctx.socket('PUB')
    sub = ctx.socket('SUB')
    sub.set_subscribe('')
    pub.bind('inproc://zoop')
    sub.connect('inproc://zoop')
    pub.send('foo')
    sub.poll(1)
    assert sub.recv() == 'foo'
