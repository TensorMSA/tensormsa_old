import inspect


def tfmsa_logger(msg):
    debug_mode = True
    if(debug_mode == True):
        print("[Func : {0}] : {1}".format(inspect.stack()[1][3], msg))

