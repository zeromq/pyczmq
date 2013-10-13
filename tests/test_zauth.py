"""
Replicates czmq test_zauth
"""

import os
import shutil
import time
from pyczmq import zmq, zauth, zcert, zctx, zpoller, zsocket, zstr


TESTDIR = ".test_zauth"
PORT_NBR = 9000


def s_can_connect(server, client):
    global PORT_NBR
    rc = zsocket.bind(server, "tcp://*:{}".format(PORT_NBR))
    assert rc == PORT_NBR
    rc = zsocket.connect(client, "tcp://localhost:{}".format(PORT_NBR))
    assert rc == 0

    zstr.send(server, "Hello World")

    # zpoller is segfaulting
    #poller = zpoller.new(client)
    #success = zpoller.wait(poller, 500) == client
    # use the zsocket.poll until resolved.
    success = zsocket.poll(client, 500)
    #zpoller.destroy(poller)

    rc = zsocket.unbind(server, "tcp://*:{}".format(PORT_NBR))
    assert rc != -1
    rc = zsocket.disconnect(client, "tcp://localhost:{}".format(PORT_NBR))
    assert rc != -1
    PORT_NBR += 1
    return success


def test_zauth(verbose=False):

    if not os.path.exists(TESTDIR):
        os.mkdir(TESTDIR)

    # Install the authenticator
    ctx = zctx.new()

    auth = zauth.new(ctx)
    zauth.set_verbose(auth, verbose)

    # A default NULL connection should always success, and not go
    # through our authentication infrastructure at all.
    server = zsocket.new(ctx, zmq.PUSH)
    client = zsocket.new(ctx, zmq.PULL)
    success = s_can_connect(server, client)
    assert success

    # When we set a domain on the server, we switch on authentication
    # for NULL sockets, but with no policies, the client connection will
    # be allowed.
    server = zsocket.new(ctx, zmq.PUSH)
    zsocket.set_zap_domain(server, 'global')
    success = s_can_connect(server, client)
    assert success

    # Blacklist 127.0.0.1, connection should fail
    zauth.deny(auth, "127.0.0.1")
    success = s_can_connect(server, client)
    assert not success

    # Whitelist our address, which overrides the blacklist
    zauth.allow (auth, "127.0.0.1")
    success = s_can_connect(server, client)
    assert success

    # Try PLAIN authentication
    password_file = os.path.join(TESTDIR, "password-file")
    fd = open(password_file, "w")
    fd.write("admin=Password\n")
    fd.close()

    zsocket.set_plain_server(server, 1)
    zsocket.set_plain_username(client, "admin")
    zsocket.set_plain_password(client, "Password")
    success = s_can_connect(server, client)
    assert not success

    zauth.configure_plain(auth, "*", password_file)
    success = s_can_connect(server, client)
    assert success

    zsocket.set_plain_password (client, "Bogus")
    success = s_can_connect(server, client)
    assert not success

    server_cert = zcert.new()
    zcert.apply(server_cert, server)
    zsocket.set_curve_server(server, 1)

    client_cert = zcert.new()
    zcert.apply(client_cert, client)
    server_key = zcert.public_txt(server_cert)
    zsocket.set_curve_serverkey(client, server_key)

    # We've not set-up any authentication, connection will fail
    success = s_can_connect(server, client)
    assert not success

    # Test CURVE_ALLOW_ANY
    zauth.configure_curve(auth, "*", zauth.CURVE_ALLOW_ANY)
    success = s_can_connect(server, client)
    assert success

    # Test full client authentication using certificates
    certificate_file = os.path.join(TESTDIR, "mycert.txt")
    zcert.save_public(client_cert, certificate_file)
    zauth.configure_curve(auth, "*", TESTDIR)
    success = s_can_connect(server, client)
    assert success

    # There is currently something wrong with manually calling
    # delete. Probably something to do with hooking the delete
    # to ffi.gc ??
    #
    #zcert.destroy(server_cert)
    #zcert.destroy(client_cert)

    # Remove the authenticator and check a normal connection works
    #zauth.destroy(auth)

    #time.sleep(0.5)

    #success = s_can_connect(server, client)
    #assert success
    #print("success")

    #zctx.destroy(ctx)

    # Delete all test files
    shutil.rmtree(TESTDIR)
