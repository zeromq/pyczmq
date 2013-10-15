"""
Test high-level API
"""

import time
from pyczmq import ffi, zmq, Context, Loop, Socket, Frame, Message
from pyczmq import zstr, zsocket


def test_context():
    # Create and destroy a context without using it
    ctx = Context()
    ctx.destroy()

    # call API functions
    ctx = Context()
    ctx.set_iothreads(1)
    ctx.set_linger(5)
    ctx.set_pipehwm(500)
    ctx.set_sndhwm(500)
    ctx.set_rcvhwm(500)
    ctx.destroy()


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
    frame.destroy()

    frame = reader.recv_frame()
    assert frame == "DEFG"
    assert not frame.more()
    frame.destroy()

    writer.destroy()
    reader.destroy()
    ctx.destroy()


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
    frame.destroy()
    copy.destroy()

    # Test zframe_new_empty
    frame = Frame()
    assert len(frame) == 0
    frame.destroy()

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
            frame.destroy()
            break
        else:
            assert len(frame) == 5
            assert frame.bytes() == "Hello"
        assert frame.more()
        frame.set_more(0)
        assert frame.more() == 0
        frame.destroy()
    assert frame_nbr == 11
    frame = input_s.recv_frame_nowait()
    assert frame is None

    ctx = ctx.destroy()


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
    msg.destroy()

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
    copy.destroy()

    msg = input_s.recv_msg()
    assert len(msg) == 10
    assert msg.content_size() == 60

    for i in range(0, 10):
        assert msg.next() == "Frame{}".format(i)
    msg.destroy()

    #TODO: continue adding remaining class function tests

    ctx.destroy()


def _test_loop(verbose=False):

    # TODO: this test function is not working properly!
    # segfault occurs when trying to call timer callback.

    def on_socket_event(loop, item, arg):
        # typically arg would be some class object containing state
        # information that would be used within this event handler.
        #input_s = ffi.from_handle(arg)
        #assert input_s.recv() == 'PING'
        assert zstr.recv(arg) == 'PING'
        return -1  # end the reactor

    def on_timer_event(loop, item, arg):
        output_s = ffi.from_handle(arg)
        output_s.send('PING')
        return 0

    ctx = Context()
    output_s = ctx.socket(zmq.PAIR)
    input_s = ctx.socket(zmq.PAIR)
    output_s.bind('inproc://zloop.test')
    input_s.connect('inproc://zloop.test')

    loop = Loop()
    loop.set_verbose(verbose)

    # After 10 msecs, send a ping message to output
    loop.timer(10, 1, on_timer_event, output_s.sock)

    poll_input = zmq.pollitem(socket=input_s.sock, events=zmq.POLLIN)

    # When we get the ping message, end the reactor
    loop.poller(poll_input, on_socket_event, input_s.sock)
    loop.set_tolerant(poll_input)

    loop.start()

    loop.destroy()
    ctx.destroy()
