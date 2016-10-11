from tfmsacore.utils.logger import tfmsa_logger
from tfmsacore import  netconf

class CNNChecker:
    def __int__(self):
        tfmsa_logger("init CNN Checker")
        self.nnid = None

    def check_sequence(self, net_id):
        """

        :return:
        """
        self.nnid = net_id
        tfmsa_logger("request nn_id : {0}".format(self.nnid))

        data = netconf.get_network_config(self.nnid)

        tfmsa_logger(data)
        tfmsa_logger(type(data))

        return self.nnid