from pyczmq import zmq, zctx, zsocket, zstr, zbeacon, zframe

def test_zbeacon():
    ctx = zctx.new()

    #  Create a service socket and bind to an ephemeral port
    service = zsocket.new(ctx, zmq.PUSH)
    port_nbr = zsocket.bind(service, "inproc://foo")
    
    #  Create beacon to broadcast our service
    announcement = str(port_nbr)
    service_beacon = zbeacon.new(9999)
    zbeacon.set_interval(service_beacon, 100)
    zbeacon.publish(service_beacon, announcement)

    #  Create beacon to lookup service
    client_beacon = zbeacon.new (9999)
    zbeacon.subscribe(client_beacon, '')

    #  Wait for at most 1/2 second if there's no broadcast networking
    beacon_socket = zbeacon.socket(client_beacon)
    zsocket.set_rcvtimeo(beacon_socket, 500)
    ipaddress = zstr.recv(beacon_socket)
    content = zframe.recv(beacon_socket)
    received_port = int(zframe.data(content))
    assert received_port == port_nbr
    zframe.destroy(content)
