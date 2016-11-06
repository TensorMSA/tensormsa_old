from tfmsacore.utils.logger import tfmsa_logger
from tfmsacore import  netconf
from tfmsacore.validation import valid_util

class CNNChecker:
    """
    check simple conf errors and guide solution
    """
    def check_sequence(self, net_id):
        """
        check conf step by step
        :return:
        """
        errMsg = []
        conf = netconf.load_conf(net_id)
        errMsg = CNNConfCheck().check_matrix_size_match(errMsg, conf)
        errMsg = CNNConfCheck().check_cnn_layer_minsize(errMsg, conf)
        errMsg = CNNConfCheck().check_cnn_layer_depth(errMsg, conf)

        tfmsa_logger(errMsg)
        return errMsg

class CNNConfCheck:
    """
    simple error check for network configuration
    """
    def check_matrix_size_match(self, errMsg, conf):
        """
        check initial matrix size
        :param errMsg: detail config error message
        :param conf: currently set network configuration
        :return: append error message on list
        """
        matrix = conf.data.matrix
        len = conf.data.datalen
        if matrix[0] * matrix[1] != len:
            errMsg.append({"code" : "000001",
                           "msg" : "Matrix size and data len unmatach"})
        return errMsg

    def check_cnn_layer_minsize(self, errMsg, conf):
        """
        simply check cnn layer is bigger than 0
        :param errMsg:
        :param conf:
        :return:
        """
        num_layers = len(conf.layer)

        for i in range(0, int(num_layers)):
            if len(conf.layer) <= 0 :
                errMsg.append({"code": "000002",
                               "msg": "CNN layer number supposed to be bigger than 0"})
        return errMsg

    def check_cnn_layer_depth(self, errMsg, conf):
        """
        check layer depth and matrix size
        :param errMsg:
        :param conf:
        :return:
        """
        num_layers = len(conf.layer)
        data_matrix = conf.data.matrix
        layers = conf.layer
        for layer in layers:
            if(layer.type != "cnn"):
                continue
            data_matrix = valid_util.cal_cnn_matrix_size(data_matrix, layer.padding, layer.maxpoolstride)
            if (int(data_matrix[0] <= int(layer.maxpoolmatrix[0]))
                or int(data_matrix[1] <= int(layer.maxpoolmatrix[1]))) :
                errMsg.append({"code": "000003",
                               "msg": "CNN layer is too deep to make matrix size smaller than 2X2"})
        return errMsg


