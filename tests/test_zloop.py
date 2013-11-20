"""
Replicates czmq test_zloop
"""

from pyczmq import ffi, zmq, zctx, zsocket, zstr, zloop


def test_zloop(verbose=False):
    ctx = zctx.new()
    output_s = zsocket.new(ctx, zmq.PAIR)
    input_s = zsocket.new(ctx, zmq.PAIR)
    zsocket.bind(output_s, 'inproc://lkj')
    zsocket.connect(input_s, 'inproc://lkj')

    @ffi.callback('zloop_fn')
    def on_socket_event(loop, item, arg):
        assert zstr.recv(item.socket) == 'PING'
        assert ffi.from_handle(arg) == 3
        return -1

    @ffi.callback('zloop_fn')
    def on_timer_event(loop, item, arg):
        zstr.send(ffi.from_handle(arg), 'PING')
        return 0

    l = zloop.new()
    zloop.set_verbose(l, verbose)

    # After 10 msecs, send a ping message to output
    zloop.timer(l, 10, 1, on_timer_event, output_s)

    # When we get the ping message, end the reactor
    poll_input = zmq.pollitem(socket=input_s, events=zmq.POLLIN)
    zloop.poller(l, poll_input, on_socket_event, 3)
    zloop.set_tolerant(l, poll_input)
    zloop.start(l)

    del l
    del ctx
