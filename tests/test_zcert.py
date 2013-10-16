"""
Replicates czmq test_zcert
"""

import os
import shutil
from pyczmq import zctx, zcert


TESTDIR = ".test_zcert"

def test_zcert():
    ctx = zctx.new()

    if os.path.exists(TESTDIR):
        # delete data from a previous test run
        shutil.rmtree(TESTDIR)
    os.mkdir(TESTDIR)

    # Create a simple certificate with metadata
    cert = zcert.new()
    zcert.set_meta(cert, "email", "ph@imatix.com")
    zcert.set_meta(cert, "name", "Pieter Hintjens")
    zcert.set_meta(cert, "organization", "iMatix Corporation")
    zcert.set_meta(cert, "version", "1")
    assert zcert.meta(cert, "email") == "ph@imatix.com"

    # Check the dup and eq methods
    shadow = zcert.dup(cert)
    assert zcert.eq(cert, shadow)
    del shadow

    # Check we can save and load certificate
    cert_file = os.path.join(TESTDIR, "mycert.txt")
    zcert.save(cert, cert_file)
    assert os.path.exists(cert_file)
    cert_secret_file = os.path.join(TESTDIR, "mycert.txt_secret")
    assert os.path.exists(cert_secret_file)

    # Load certificate, will in fact load secret one
    shadow = zcert.load(cert_file)
    assert shadow
    assert zcert.eq(cert, shadow)
    del shadow

    del ctx

    # Delete all test files
    shutil.rmtree(TESTDIR)
