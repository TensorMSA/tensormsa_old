import inspect
from TensorMSA import const


def tfmsa_logger(msg):

    if(const.LOG_MODE == True):
        print("[Func : {0}] : {1}".format(inspect.stack()[1][3], msg))

