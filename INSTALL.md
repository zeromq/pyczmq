
You need zmq >= 4 and czmq >= 2.0.2.  Download and build with
configure/make/make-install.

You will need libffi, on ubuntu this can be installed with 'sudo
apt-get install libffi-dev'.

Clone pyczmq repo:

  git clone https://github.com/michelp/pyczmq.git

and run '. bootstrap' This will create a virtualenv for you and
install the necessary dependencies.

If you want to run the tests, install the 'nose' package and run
'nosetests'.

