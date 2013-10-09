import new
from pyczmq import _cffi, zctx, zsocket, zsockopt, zstr, zframe, zmsg, zbeacon, zloop


class Socket(object):

    def __init__(self, ctx, typ):
        self.sock = zsocket.new(ctx, typ)

    def send(self, msg):
        return zstr.send(self.sock, msg)

    def recv(self):
        return zstr.recv(self.sock)

    def recv_nowait(self):
        return zstr.recv_nowait(self.sock)

    def send_frame(self, frame):
        return zframe.send(self.sock, frame)

    def recv_frame(self):
        return zframe.recv(self.sock)

    def recv_frame_nowait(self):
        return zframe.recv_nowait(self.sock)

    def send_msg(self, msg):
        return zmsg.send(msg)

    def connect(self, endpoint):
        return zsocket.connect(self.sock, endpoint)

    def disconnect(self, endpoint):
        return zsocket.disconnect(self.sock, endpoint)

    def bind(self, endpoint):
        return zsocket.bind(self.sock, endpoint)

    def unbind(self, endpoint):
        return zsocket.unbind(self.sock, endpoint)

    def poll(self, timeout=0):
        return zsocket.poll(self.sock, timeout)

    def __getattr__(self, name):
        if name in dir(zsockopt):
            return lambda *args: getattr(zsockopt, name)(self.sock, *args)
        raise AttributeError(name)

    def __repr__(self):
        return '<Socket %s>' % zsocket.type_str(self.sock)


class Context(object):

    def __init__(self, iothreads=1):
        self.ctx = zctx.new()
        zctx.set_iothreads(self.ctx, iothreads)
    
    def socket(self, typ):
        if isinstance(typ, basestring):
            typ = zsocket.types[typ]
        return Socket(self.ctx, typ)


# TODO below

class Loop(object):
    
    def __init__(self):
        self.loop = zloop.new()

    def start(self):
        zloop.start(self.loop)

    def poller(self, item, handler, arg=None):
        callback = _cffi.ffi.callback('zloop_fn', handler)
        zloop.poller(self.loop, item, callback, arg)


class Beacon(object):
    
    def __init__(self):
        self.loop = zbeacon.new()
