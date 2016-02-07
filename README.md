# Pyczmq
Pyczmq is a Python wrapper around the CZMQ zeromq bindings.

[![Build Status](https://travis-ci.org/zeromq/pyczmq.png?branch=master)](https://travis-ci.org/zeromq/pyczmq)

## Overview

Pyczmq exposes CZMQ functions via the cffi library's ABI access mode.  No compiler is required to use it.  The czmq library is accessed with dlopen and a set of parsed function declarations.

This is still a work in progress, not all of the API is fully wrapped yet. Most of the core context, socket, socket option, polling, beacon, auth, and cert functions are provided. Some functions will probably not be wrapped, notably those that provide duplicate functionality to built-in python type or libraries like zlist, zhash, zsys, zclock, zdir, etc.


## Building and Installing

There are two methods for installing pyczmq.

### Option 1 - Use the Cheese Shop

This is the easiest option for most users. If you have all the dependencies then it is as simple as:

    [sudo] pip install pyczmq

NOTE: This version may not be as up to date as the Github master.


### Option 2 - Use Github

This option would typically be used by users and contributing developers who want access to the most up to date version.


#### Dependencies

On Ubuntu you need the following packages (Other OSes may use a different package name) which are typicall installed using 'sudo apt-get install _package_':

    libffi-dev
    python-dev
    python-virtualenv

The following Python packages are required which are typically installed using 'sudo pip install _package_':

    cffi
    nose

Libsodium provides security for ZMQ:

    git clone git://github.com/jedisct1/libsodium.git
    cd libsodium
    ./autogen.sh
    ./configure && make check
    sudo make install
    sudo ldconfig
    cd ..

The ZMQ core library:

    git clone git://github.com/zeromq/libzmq.git
    cd libzmq
    ./autogen.sh
    ./configure && make check
    sudo make install
    sudo ldconfig
    cd ..

The high-level CZMQ library:

    git clone git://github.com/zeromq/czmq.git
    cd czmq
    ./autogen.sh
    ./configure && make check
    sudo make install
    sudo ldconfig
    cd ..


#### Pyczmq Installation

    git clone git://github.com/zeromq/pyczmq.git
    cd pyczmq
    sudo python setup.py install


#### Testing

The pyczmq tests are run using the *nose* testing package. The tests are run from the top level pyczmq directory using:

    nosetests [-v]


To report an issue, use the [Pyczmq issue tracker](https://github.com/zeromq/pyczmq/issues) at github.com.

## Details

All CZMQ functions can be accessed directly via the low-level cffi
binding, ie:

  - pyczmq.C.zctx_new

  - pyczmq.C.zsocket_bind

  - pyczmq.C.zstr_send

  - etc...

Functions also have aliases in a module level namespace interface, so:

  - pyczmq.C.zctx_new is pyczmq.zctx.new (with caveat, see below)

  - pyczmq.C.zsocket_bind is pyczmq.zsocket.bind

  - pyczmq.C.zstr_send is pyczmq.zstr.send

  - etc...

For example a simple PUSH/PULL socket pipeline::

    from pyzmq import zctx, zsocket, zstr, zmq

    ctx = zctx.new()
    push = zsocket.new(ctx, zmq.PUSH)
    pull = zsocket.new(ctx, zmq.PULL)
    zsocket.bind(push, 'inproc://test')
    zsocket.connect(pull, 'inproc://test')
    zstr.send(push, 'foo')
    assert zstr.recv(pull) == 'foo'
    zstr.send(push, 'foo')
    zsocket.poll(pull, 1)
    assert zstr.recv_nowait(pull) == 'foo'

Some of the 'new' functions in the module namespaces (like pyczmq.zctx.new) are wrappers that plug into Python's garbage collector, so you typically never need to explicitly destroy objects if you use the namespace interface.

Therefore, pyczmq.zctx.new isn't *really* pyczmq.C.zmq_new, but the effect is exactly the same.  If you use the "raw" C binding interface pyczmq.C.zctx_new, however, you must explicitly garbage collect your own resources by calling the coresponding destroy method (pyczmq.C.zctx_destroy, etc.).

Some 'new' functions do not do this wrapping behavior, because they are meant to be destroyed by czmq. zmsg objects for example are destroyed by zmsg_send, and zframe objects have their ownership taken over by various functions in zmsg and are destroyed when the msg is sent and destroyed.  If you create these objects and don't in turn call the functions that destroy them, you must explicitly destroy them yourself with zmsg.destroy or zframe.destroy.


## API Documentation

The documentation for this binding can be found at readthedocs:

    http://pyczmq.readthedocs.org/
