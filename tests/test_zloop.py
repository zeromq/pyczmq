"""
Replicates czmq test_zloop
"""

from pyczmq import zmq, zctx, zsocket, zstr, zloop


def test_zloop(verbose=False):
    ctx = zctx.new()
    output_s = zsocket.new(ctx, zmq.PAIR)
    input_s = zsocket.new(ctx, zmq.PAIR)
    zsocket.bind(output_s, 'inproc://lkj')
    zsocket.connect(input_s, 'inproc://lkj')

    @zloop.poll_callback
    def on_socket_event(loop, item, arg):
        assert zstr.recv(item.socket) == 'PING'
        assert arg == 3
        return -1

    @zloop.timer_callback
    def on_timer_event(loop, item, arg):
        zstr.send(arg, 'PING')
        return 0

    @zloop.timer_callback
    def on_cancel_timer_event(loop, item, arg):
        cancel_timer_id = arg
        rc = zloop.timer_end(loop, cancel_timer_id)
        assert (rc == 0)
        return 0

    l = zloop.new()
    zloop.set_verbose(l, verbose)

    # create a timer that will be cancelled
    cancel_timer_id = zloop.timer(l, 1000, 1, on_timer_event, None)
    zloop.timer(l, 5, 1, on_cancel_timer_event, cancel_timer_id)

    # After 10 msecs, send a ping message to output
    zloop.timer(l, 20, 1, on_timer_event, output_s)

    # When we get the ping message, end the reactor
    poll_input = zmq.pollitem(socket=input_s, events=zmq.POLLIN)
    zloop.poller(l, poll_input, on_socket_event, 3)
    zloop.poller_set_tolerant(l, poll_input)
    zloop.start(l)

    del l
    del ctx
