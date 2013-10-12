from pyczmq import zmq


def test_zmq():
    version = zmq.version()
    assert version
    assert len(version) == 3
    assert version[0] in (4, 3)
