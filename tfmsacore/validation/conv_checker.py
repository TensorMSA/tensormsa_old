from tfmsacore.utils.logger import tfmsa_logger
from tfmsacore import  netconf

import tensorflow as tf
# from tfmsacore.utils import JsonDataConverter,CusJsonEncoder
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
import numpy as np

class gVal:
    log = "Y"

class CNNChecker:
    def __int__(self):
        tfmsa_logger("init CNNChecker")
        self.nnid = None

    def check_sequence(self, net_id):
        """

        :return:
        """
        self.nnid = net_id
        errMsg = "S"
        tfmsa_logger("request nn_id : {0}".format(self.nnid))

        # data = netconf.get_network_config(self.nnid)
        conf_ori = netconf.load_ori_conf(self.nnid)
        print("conf_ori", conf_ori)

        conf = netconf.load_conf(self.nnid)
        # tfmsa_logger(conf.data)
        tfmsa_logger(type(conf))

        # Matrix Check
        if errMsg == "S":
            errMsg = CNNConfCheck().check_Matrix(conf)

        if errMsg == "S":
            errMsg = CNNConfCheck().check_Filter_MinValue(conf)

        gValue = gVal()
        if gValue.log == "Y":
            print("====================================================================")
            print("errMsg", errMsg)
            print("====================================================================")

        return self.nnid



class CNNConfCheck:

    def __int__(self):
        self.msg = "Y"

    def check_Matrix(self, conf):
        try:
            errMsg = "S"
            matrix = conf.data.matrix
            len = conf.data.datalen
            if matrix[0] * matrix[1] <> len:
                errMsg = "Error[000001]: Matrix is not Valid"

            gValue = gVal()
            if gValue.log == "Y" and errMsg == "S":
                msg = "check_Matrix Clear..........matrix[0]="+str(matrix[0])+" matrix[1]="+str(matrix[1])+" len="+str(len)
                print(msg)
        except Exception as e:
            print("Exception check_Matrix : ", e)
            errMsg = e

        return errMsg

    def check_Filter_MinValue(self, conf):
        try:
            gValue = gVal()
            errMsg = "S"
            num_layers = len(conf.layer)

            for i in range(0, int(num_layers)):
                ft = conf.layer[i]
                if len(ft.cnnfilter) >0 and ft.cnnfilter[0] < 2:
                    errMsg = "Error[000004]: Filter must be larger than [2, 2] Filter:[" + str(ft.cnnfilter) + "," + str(ft.cnnfilter) + "]"

                if gValue.log == "Y" and errMsg == "S":
                    msg = "check_Filter_MinValue Clear..........len(ft.cnnfilter)="+str(len(ft.cnnfilter))+"  ft.cnnfilter="+ str(ft.cnnfilter)
                    print(msg)
        except Exception as e:
            print("Exception check_Filter : ", e)
            errMsg = e

        return errMsg

    def check_Filter_Size(self, matrix, cnnfilter):
        try:
            gValue = gVal()
            errMsg = "S"

            if matrix[0] < cnnfilter[0] or matrix[1] < cnnfilter[1]:
                errMsg = "Error[000002]: Filter must not be larger than the input: Filter:[" + str(
                    cnnfilter) + "," + str(cnnfilter) + "] Input: " + str(matrix)

            if gValue.log == "Y" and errMsg == "S":
                msg = "check_Filter_Size Clear..........cnnfilter="+str(cnnfilter)+"  matrix="+ str(matrix)
                print(msg)
        except Exception as e:
            print("Exception check_Filter : ", e)
            errMsg = e

        return errMsg

class NetworkClass:
    def __int__(self):
        self.msg = "Y"

    def get_CNN_train(self, conf, inData):
        errMsg = "S"
        matrix = conf.data.matrix

        learnrate = conf.data.learnrate
        num_layers = len(conf.layer)

        network = input_data(shape=[None, matrix[0], matrix[1], 1], name='input')

        for i in range(0, int(num_layers)):
            data = conf.layer[i]
            print(data.type)
            if (data.type == "cnn"):
                errMsg = CNNConfCheck().check_Filter_Size( matrix, data.cnnfilter )

                if errMsg == "S":
                    network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active),
                                      regularizer=data.regualizer)
                    network = max_pool_2d(network, data.maxpoolmatrix)
                    network = local_response_normalization(network)

                    matrix[0] = network.get_shape()[1].value
                    matrix[1] = network.get_shape()[2].value

            elif (data.type == "drop"):
                network = fully_connected(network, data.node_in_out[0], activation=str(data.active))
                network = dropout(network, int(data.droprate))
                network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
                network = dropout(network, int(data.droprate))

            elif (data.type == "out"):
                network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
                network = regression(network, optimizer='adam', learning_rate=learnrate,
                                     loss='categorical_crossentropy', name='target')

            elif (data.type == "fully"):
                network = fully_connected(network, data.node_in_out[1], activation=str(data.active))

                # else:
                #     raise SyntaxError("there is no such kind of nn type : " + str(data.active))

        return network, errMsg