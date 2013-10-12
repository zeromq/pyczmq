from pyczmq import (
    _cffi,
    zmq,
    zctx,
    zsocket,
    zsockopt,
    zstr,
    zframe,
    zmsg,
    zbeacon,
    zloop,
    )


class Frame(object):
    """
    Object wrapper around a zframe
    """

    MORE = zframe.MORE
    REUSE = zframe.REUSE
    DONTWAIT = zframe.DONTWAIT

    __slots__ = ('frame',)

    def __init__(self, data=None, frame=None):
        if data is not None:
            self.frame = zframe.new(data)
        elif frame is not None:
            self.frame = frame
        else:
            self.frame = zframe.new_empty()

    def __str__(self):
        return zframe.strdup(self.frame)

    def __len__(self):
        return zframe.size(self.frame)

    def __eq__(self, other):
        if isinstance(other, str):
            return zframe.streq(self.frame, other)
        elif isinstance(other, Frame):
            return zframe.eq(self.frame, other.frame)
        return zframe.eq(self.frame, other)

    @property
    def bytes(self):
        return zframe.data(self.frame)

    def destroy(self):
        zframe.destroy(self.frame)
        self.frame = None

    def dup(self):
        return zframe.dup(self.frame)

    def strhex(self):
        return zframe.strhex(self.frame)

    def reset(self, data):
        return zframe.reset(data, len(data))

    def more(self):
        return zframe.more(self.frame)

    def set_more(self, val=0):
        if val:
            val = 1
        return zframe.set_more(self.frame, val)


class Message(object):
    """
    Object wrapper around a zmsg
    """

    __slots__ = ('msg',)

    def __init__(self, msg):
        self.msg = msg

    def __len__(self):
        return zmsg.size(self.msg)

    def destroy(self):
        zmsg.destroy(self.msg)
        self.msg = None

    def content_size(self):
        return zmsg.content_size(self.msg)

    def push(self, frame):
        if isinstance(frame, str):
            return zmsg.pushstr(self.msg, frame)
        if isinstance(frame, Frame):
            frame = frame.frame
        return zmsg.push(self.msg, frame)

    def append(self, frame):
        if isinstance(frame, str):
            return zmsg.addstr(self.msg, frame)
        if isinstance(frame, Frame):
            frame = frame.frame
        return zmsg.append(self.msg, frame)

    def pop(self):
        return Frame(frame=zmsg.pop(self.msg))

    def popstr(self):
        return zmsg.popstr(self.msg)

    def first(self):
        return Frame(frame=zmsg.first(self.msg))

    def next(self):
        return Frame(frame=zmsg.next(self.msg))

    def last(self):
        return Frame(frame=zmsg.last(self.msg))

    def __iter__(self):
        n = self.next()
        while True:
            if n is None:
                raise StopIteration
            yield n
            n = self.next()


class Socket(object):
    """Wrapper class around zsocket/zsockopt
    """

    __slots__ = ('sock',)

    def __init__(self, ctx, typ):
        self.sock = zsocket.new(ctx, typ)

    def send(self, msg):
        return zstr.send(self.sock, msg)

    def recv(self):
        return zstr.recv(self.sock)

    def recv_nowait(self):
        return zstr.recv_nowait(self.sock)

    def send_frame(self, frame):
        if isinstance(frame, Frame):
            frame = frame.frame
        return zframe.send(self.sock, frame)

    def recv_frame(self):
        return Frame(frame=zframe.recv(self.sock))

    def recv_frame_nowait(self):
        return Frame(frame=zframe.recv_nowait(self.sock))

    def send_msg(self, msg):
        if isinstance(msg, Message):
            msg = msg.msg
        return zmsg.send(self.sock, msg)

    def recv_msg(self):
        return Message(zmsg.recv(self.sock))

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
    """
    Object wrapper around a zctx
    """

    def __init__(self, iothreads=1):
        self.ctx = zctx.new()
        zctx.set_iothreads(self.ctx, iothreads)

    def socket(self, typ):
        if isinstance(typ, basestring):
            typ = zmq.types[typ]
        return Socket(self.ctx, typ)


# TODO below

class Loop(object):
    """
    Object wrapper around a zloop
    """

    def __init__(self):
        self.loop = zloop.new()

    def start(self):
        zloop.start(self.loop)

    def poller(self, item, handler, arg=None):
        callback = _cffi.ffi.callback('zloop_fn', handler)
        arg_handle = _cffi.ffi.new_handle(arg)
        zloop.poller(self.loop, item, callback, arg_handle)

    def timer(self, delay, times, handler, arg=None):
        callback = _cffi.ffi.callback('zloop_fn', handler)
        arg_handle = _cffi.ffi.new_handle(arg)
        zloop.timer(self.loop, delay, times, callback, arg_handle)



class Beacon(object):

    def __init__(self):
        self.loop = zbeacon.new()
