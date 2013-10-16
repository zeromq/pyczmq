from pyczmq import (
    zmq,
    zctx,
    zsocket,
    zstr,
    zframe,
    zmsg,
    zbeacon,
    zloop,
    )
from pyczmq._cffi import ffi


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

    def bytes(self):
        return zframe.data(self.frame)[:]

    def dup(self):
        return Frame(frame=zframe.dup(self.frame))

    def strhex(self):
        return zframe.strhex(self.frame)

    def reset(self, data):
        zframe.reset(self.frame, data)

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

    def __init__(self, msg=None):
        if msg:
            self.msg = msg
        else:
            self.msg = zmsg.new()

    def __len__(self):
        return zmsg.size(self.msg)

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

    def dup(self):
        return Message(msg=zmsg.dup(self.msg))

    def first(self):
        return Frame(frame=zmsg.first(self.msg))

    def next(self):
        return Frame(frame=zmsg.next(self.msg))

    def last(self):
        return Frame(frame=zmsg.last(self.msg))

    def save(self, filename):
        fd = open(filename, 'w')
        rc = zmsg.save(self.msg, ffi.cast("FILE *", filename))
        if rc != 0:
            print("Error saving msg to file")
        fd.close()

    def load(self, filename):
        fd = open(filename, 'r')
        if self.msg:
            self.destroy()
        msg = zmsg.load(ffi.NULL, ffi.cast("FILE *", filename))
        if msg is not ffi.NULL:
            self.msg = msg
        fd.close()

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

    __slots__ = ('sock', 'ctx')

    def __init__(self, ctx, typ):
        self.ctx = ctx
        self.sock = zsocket.new(ctx, typ)

    def __getattr__(self, name):
        if name in dir(zsocket):
            return lambda *args: getattr(zsocket, name)(self.sock, *args)
        raise AttributeError(name)

    def __repr__(self):
        return '<Socket {}>'.format(zsocket.type_str(self.sock))

    def __str__(self):
        return '{} socket'.format(zsocket.type_str(self.sock))

    def type(self):
        return zsocket.type_str(self.sock)

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

    def send(self, msg):
        return zstr.send(self.sock, msg)

    def send_frame(self, frame, flags=0):
        if isinstance(frame, Frame):
            frame = frame.frame
        return zframe.send(frame, self.sock, flags)

    def send_msg(self, msg):
        if isinstance(msg, Message):
            msg = msg.msg
        return zmsg.send(msg, self.sock)

    def recv(self):
        return zstr.recv(self.sock)

    def recv_nowait(self):
        return zstr.recv_nowait(self.sock)

    def recv_frame(self):
        f = zframe.recv(self.sock)
        if f:
            f = Frame(frame=f)
        return f

    def recv_frame_nowait(self):
        f = zframe.recv_nowait(self.sock)
        if f:
            f = Frame(frame=f)
        return f

    def recv_msg(self):
        return Message(zmsg.recv(self.sock))


class Context(object):
    """
    Object wrapper around a zctx
    """

    def __init__(self, iothreads=1):
        self.ctx = zctx.new()
        zctx.set_iothreads(self.ctx, iothreads)

    def set_iothreads(self, thread_count):
        zctx.set_iothreads(self.ctx, thread_count)

    def set_linger(self, msecs):
        zctx.set_linger(self.ctx, msecs)

    def set_pipehwm(self, hwm):
        zctx.set_pipehwm(self.ctx, hwm)

    def set_sndhwm(self, hwm):
        zctx.set_sndhwm(self.ctx, hwm)

    def set_rcvhwm(self, hwm):
        zctx.set_rcvhwm(self.ctx, hwm)

    def socket(self, typ):
        if isinstance(typ, basestring):
            typ = zmq.types[typ]
        return Socket(self.ctx, typ)


class Loop(object):
    """
    Object wrapper around a zloop
    """

    def __init__(self):
        self.loop = zloop.new()

    def set_tolerant(self, item):
        zloop.set_tolerant(self.loop, item)

    def set_verbose(self, verbose):
        zloop.set_verbose(self.loop, verbose)

    def start(self):
        zloop.start(self.loop)

    def poller(self, poll_item, handler, arg=None):
        callback = ffi.callback('zloop_fn', handler)
        arg_handle = ffi.new_handle(arg)
        return zloop.poller(self.loop, poll_item, callback, arg_handle)

    def poller_end(self, poll_item):
        return zloop.poller_end(self.loop, poll_item)

    def timer(self, delay, times, handler, arg=None):
        callback = ffi.callback('zloop_fn', handler)
        arg_handle = ffi.new_handle(arg)
        return zloop.timer(self.loop, delay, times, callback, arg_handle)

    def timer_end(self, arg):
        arg_handle = ffi.new_handle(arg)
        zloop.timer_end(self.loop, arg_handle)


class Beacon(object):

    def __init__(self):
        self.beacon = zbeacon.new()
