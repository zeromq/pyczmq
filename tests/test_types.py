"""
Test high-level API
"""

import time
from pyczmq import ffi, zmq, Context, Loop, Frame, Message, zsocket

# debug only
from pyczmq import zloop


def test_context():
    # Create and destroy a context without using it
    ctx = Context()
    del ctx

    # call API functions
    ctx = Context()
    ctx.set_iothreads(1)
    ctx.set_linger(5)
    ctx.set_pipehwm(500)
    ctx.set_sndhwm(500)
    ctx.set_rcvhwm(500)
    del ctx


def test_socket():
    ctx = Context()

    # Create a detached thread, let it run
    interf = "*"
    domain = "localhost"
    service = 5560

    writer = ctx.socket(zmq.PUSH)
    assert writer
    reader = ctx.socket(zmq.PULL)
    assert reader
    assert writer.type() == "PUSH"
    assert reader.type() == "PULL"
    rc = writer.bind("tcp://{}:{}".format(interf, service))
    assert rc == service


    # Check unbind
    rc = writer.unbind("tcp://{}:{}".format(interf, service))
    assert rc == 0

    # In some cases and especially when running under Valgrind, doing
    # a bind immediately after an unbind causes an EADDRINUSE error.
    # Even a short sleep allows the OS to release the port for reuse.
    time.sleep(0.1)

    # Bind again
    rc = writer.bind("tcp://{}:{}".format(interf, service))
    assert rc == service


    rc = reader.connect("tcp://{}:{}".format(domain, service))
    assert rc == 0
    writer.send("HELLO")
    message = reader.recv()
    assert message
    assert message == "HELLO"

    # Test binding to ports
    port = writer.bind("tcp://{}:*".format(interf))
    assert (port >= zsocket.DYNFROM and port <= zsocket.DYNTO)

    assert writer.poll(100) == False

    rc = reader.connect("txp://{}:{}".format(domain, service))
    assert rc == -1

    # Test sending frames to socket
    frame = Frame("ABC")
    rc = writer.send_frame(frame, Frame.MORE)
    assert rc == 0
    frame = Frame("DEFG")
    rc = writer.send_frame(frame)
    assert rc == 0

    frame = reader.recv_frame()
    assert frame == "ABC"
    assert frame.more()
    del frame

    frame = reader.recv_frame()
    assert frame == "DEFG"
    assert not frame.more()
    del frame

    del writer
    del reader
    del ctx


def test_frame():
    ctx = Context()
    test_endpoint = 'inproc://zframe.test'
    output_s = ctx.socket(zmq.PAIR)
    rc = output_s.bind(test_endpoint)
    assert rc >= 0
    input_s = ctx.socket(zmq.PAIR)
    rc = input_s.connect(test_endpoint)
    assert rc == 0

    # Send five different frames, test ZFRAME_MORE
    for i in range(0, 5):
        frame = Frame("Hello")
        rc = output_s.send_frame(frame, Frame.MORE)
        assert rc == 0, "error sending frame rc={}, {}".format(rc, zmq.strerror(zmq.errno()))

    # Send same frame five times, test ZFRAME_REUSE
    frame = Frame("Hello")
    for i in range(0, 5):
        rc = output_s.send_frame(frame, Frame.MORE + Frame.REUSE)
        assert rc == 0, "error sending reused frame rc={}, {}".format(rc, zmq.strerror(zmq.errno()))

    copy = frame.dup()
    assert frame == copy

    frame.reset("")
    assert frame != copy
    assert len(copy) == 5
    del frame
    del copy

    # Test zframe_new_empty
    frame = Frame()
    assert len(frame) == 0
    del frame

    # Send END frame
    frame = Frame("NOT")
    frame.reset("END")
    hex_string = frame.strhex()
    assert hex_string == "454E44"

    frame_bytes = frame.bytes()
    assert frame_bytes == "END"

    string = str(frame)
    assert string == "END"
    rc = output_s.send_frame(frame)
    assert rc == 0

    # Read and count until we receive END
    frame_nbr = 0
    while True:
        frame = input_s.recv_frame()
        frame_nbr += 1
        if frame == "END":
            del frame
            break
        else:
            assert len(frame) == 5
            assert frame.bytes() == "Hello"
        assert frame.more()
        frame.set_more(0)
        assert frame.more() == 0
        del frame
    assert frame_nbr == 11
    frame = input_s.recv_frame_nowait()
    assert frame is None

    del ctx


def test_message():
    ctx = Context()

    test_endpoint = "inproc://zmsg.test"
    output_s = ctx.socket(zmq.PAIR)
    rc = output_s.bind(test_endpoint)
    assert rc >= 0
    input_s = ctx.socket(zmq.PAIR)
    rc = input_s.connect(test_endpoint)
    assert rc == 0

    msg = Message()

    foo = Frame('Hello')
    msg.push(foo)
    assert len(msg) == 1
    assert msg.content_size() == 5

    rc = output_s.send_msg(msg)
    assert rc == 0

    msg = input_s.recv_msg()
    assert len(msg) == 1
    assert msg.content_size() == 5
    del msg

    msg = Message()
    for i in range(0, 10):
        rc = msg.append("Frame{}".format(i))
        assert rc == 0

    copy = msg.dup()
    rc = output_s.send_msg(copy)
    assert rc == 0
    rc = output_s.send_msg(msg)
    assert rc == 0

    copy = input_s.recv_msg()
    assert len(copy) == 10
    assert copy.content_size() == 60
    del copy

    msg = input_s.recv_msg()
    assert len(msg) == 10
    assert msg.content_size() == 60

    for i in range(0, 10):
        assert msg.next() == "Frame{}".format(i)
    del msg

    #TODO: continue adding remaining class function tests

    del ctx




# TODO: this test function is not working properly!
# Segfault occurs when trying to call timer callback.
# Problem occurs when CZMQ calls the handler function.
# Perhaps we need to maintain a reference to the cdata
# returned from ffi.new_handle(arg)
def _test_loop(verbose=False):

    @zloop.timer_callback
    def on_cancel_timer_event(loop, timer_id, arg):
        cancel_timer_id = arg
        zloop.timer_end(loop, cancel_timer_id)
        return 0

    @zloop.timer_callback
    def on_timer_event(loop, item, arg):
        output_s = ffi.from_handle(arg)
        output_s.send('PING')
        return 0

    @zloop.poll_callback
    def on_socket_event(loop, item, arg):
        # typically arg would be some class object containing state
        # information that would be used within this event handler.
        input_s = ffi.from_handle(arg)
        assert input_s.recv() == 'PING'
        return -1  # end the reactor


    ctx = Context()
    output_s = ctx.socket(zmq.PAIR)
    input_s = ctx.socket(zmq.PAIR)
    output_s.bind('inproc://zloop.test')
    input_s.connect('inproc://zloop.test')

    loop = Loop()
    loop.set_verbose(verbose)

    # create a timer that will be cancelled
    cancel_timer_id = loop.timer(1000, 1, on_timer_event, None)
    loop.timer(5, 1, on_cancel_timer_event, cancel_timer_id)

    # After 10 msecs, send a ping message to output
    loop.timer(20, 1, on_timer_event, output_s.sock)

    poll_input = zmq.pollitem(socket=input_s.sock, events=zmq.POLLIN)

    # When we get the ping message, end the reactor
    loop.poller(poll_input, on_socket_event, input_s.sock)
    loop.set_tolerant(poll_input)

    loop.start()

    del loop
    del ctx
