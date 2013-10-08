from pyczmq import zctx

def test_ctx():
    zctx.test(True)
    ctx = zctx.new()
    zctx.set_iothreads(ctx, 2)
    zctx.set_iothreads(ctx, 1)
    zctx.set_linger(ctx, 1)
    zctx.set_pipehwm(ctx, 500)
    zctx.set_rcvhwm(ctx, 500)
    underlying = zctx.underlying(ctx)
    del ctx

    

