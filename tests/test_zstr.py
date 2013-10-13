"""
Replicates czmq test_zstr
"""

from pyczmq import zmq, zctx, zsocket, zstr

def test_zstr():
    ctx = zctx.new()
    test_endpoint = 'inproc://zstr.test'
    output_s = zsocket.new(ctx, zmq.PAIR)
    zsocket.bind(output_s, test_endpoint)
    input_s = zsocket.new(ctx, zmq.PAIR)
    zsocket.connect(input_s, test_endpoint)

    # Send ten strings, five strings with MORE flag and then END
    for i in range(0, 10):
        rc = zstr.send(output_s, "this is string {}".format(i))
        assert(rc == 0)
    zstr.sendx(output_s, "This", "is", "almost", "the", "very", "END")

    # Read and count until we receive END
    string_nbr = 0
    while True:
        string = zstr.recv(input_s)
        if string == "END":
            break
        string_nbr += 1
    assert(string_nbr == 15)

