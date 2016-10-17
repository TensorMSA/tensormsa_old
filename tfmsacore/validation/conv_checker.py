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
            network, errMsg = NetworkClass().get_CNN_train(conf)

        gValue = gVal()
        if gValue.log == "Y":
            print("====================================================================")
            print("errMsg", errMsg)
            print("====================================================================")

        return self.nnid



class CNNConfCheck:

    def __int__(self):
        self.msg = "Y"

    def check_CNN_Matrix(self, conf):
        try:
            errMsg = "S"
            gValue = gVal()

            matrix = conf.data.matrix
            x_shape = conf.data.x_shape # [4,5] 4 row, 5 column indata
            y_shape = conf.data.y_shape # [4,2] 4 row, 2 column outdata

            if matrix[0] * matrix[1] < x_shape[1]:
                errMsg = "Error[000004]: Matrix is not Valid(Small)"
            elif (x_shape[0]*x_shape[1])%(matrix[0] * matrix[1]) <> 0:
                errMsg = "Error[000004]: Matrix is not Valid"

            gValue = gVal()
            # if gValue.log == "Y" and errMsg == "S":
            #     msg = "check_Matrix Clear..........matrix[0]="+str(matrix[0])+" matrix[1]="+str(matrix[1])
            #     print(msg)

            if gValue.log == "Y":
                print("conf.data.matrix", conf.data.matrix)
                print("conf.data.x_shape", conf.data.x_shape)
                print("conf.data.y_shape", conf.data.y_shape)
        except Exception as e:
            print("Exception check_Matrix : ", e)
            errMsg = e

        return errMsg

    def check_CNN_Filter_MinValue(self, conf):
        try:
            gValue = gVal()
            errMsg = "S"
            num_layers = len(conf.layer)

            for i in range(0, int(num_layers)):
                ft = conf.layer[i]
                if len(ft.cnnfilter) >0 and ft.cnnfilter[0] < 2:
                    errMsg = "Error[000001]: Filter must be larger than [2, 2] Filter:[" + str(ft.cnnfilter) + "," + str(ft.cnnfilter) + "]"

                # if gValue.log == "Y" and errMsg == "S" and len(ft.cnnfilter) >0:
                #     msg = "check_Filter_MinValue Clear.........."+str(ft.type)+"  len(ft.cnnfilter)="+str(len(ft.cnnfilter))+"  ft.cnnfilter="+ str(ft.cnnfilter)
                #     print(msg)
        except Exception as e:
            print("Exception check_Filter_MinValue : ", e)
            errMsg = e

        return errMsg

    def check_CNN_Filter_Size(self, mat_x, mat_y, cnnfilter):
        try:
            gValue = gVal()
            errMsg = "S"
            if mat_x < cnnfilter[0] or mat_y < cnnfilter[1]:
                errMsg = "Warnning[000003]: Filter must not be larger than the input: Filter:[" + str(
                    cnnfilter) + "," + str(cnnfilter) + "] Input: [" + str(mat_x)+", "+ str(mat_y)+"]"

            if gValue.log == "Y" and errMsg == "S":
                msg = "get_CNN_train Clear..........filtersize="+str(cnnfilter)+"  matrix="+ str(mat_x)+", "+ str(mat_y)+"]"
                print(msg)
        except Exception as e:
            print("Exception check_Filter_Size : ", e)
            errMsg = e
        return errMsg

    def check_CNN_Droprate(self, droprate):
        try:
            gValue = gVal()
            errMsg = "S"

            if len(droprate) == 0:
                errMsg = "Error[000002]: Droprate is Null("+str(droprate)+")"

            # if gValue.log == "Y" and errMsg == "S":
            #     msg = "get_CNN_train Clear..........droprate="+str(droprate)
            #     print(msg)
        except Exception as e:
            print("Exception check_Droprate : ", e)
            errMsg = e

        return errMsg

class NetworkClass:
    def __int__(self):
        self.msg = "S"

    def get_CNN_train(self, conf):
        gValue = gVal()
        errMsg = "S"
        outFlag = "N"
        mat_x = conf.data.matrix[0]
        mat_y = conf.data.matrix[1]

        learnrate = conf.data.learnrate
        num_layers = len(conf.layer)

        if errMsg == "S":
            errMsg = CNNConfCheck().check_CNN_Matrix(conf)

        if errMsg == "S":
            errMsg = CNNConfCheck().check_CNN_Filter_MinValue(conf)

        for i in range(0, int(num_layers)):
            data = conf.layer[i]
            if (data.type == "input"):
                network = input_data(shape=[None, mat_x, mat_y, 1], name='input')
            elif (data.type == "cnn"):
                if errMsg == "S":
                    errMsg = CNNConfCheck().check_CNN_Filter_Size( mat_x, mat_y, data.cnnfilter )

                if errMsg == "S":
                    if gValue.log == "Y":
                        print("get_CNN_train Clear.........."+str(data.type))
                    network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active),regularizer=data.regualizer)
                    network = max_pool_2d(network, data.maxpoolmatrix)
                    network = local_response_normalization(network)

                    mat_x = network.get_shape()[1].value
                    mat_y = network.get_shape()[2].value
            elif (data.type == "drop"):
                if errMsg == "S":
                    errMsg = CNNConfCheck().check_CNN_Droprate(data.droprate)

                if errMsg == "S":
                    if gValue.log == "Y":
                        print("get_CNN_train Clear.........." + str(data.type))
                    network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
                    network = dropout(network, float(data.droprate))

            elif (data.type == "out"):
                if gValue.log == "Y":
                    print("get_CNN_train Clear.........." + str(data.type))
                network = fully_connected(network, conf.data.y_shape[1], activation=str(data.active))
                network = regression(network, optimizer='adam', learning_rate=learnrate,
                                     loss='categorical_crossentropy', name='target')
                outFlag = "Y"


        if outFlag == "N":
            errMsg = "Error[000003]: Out Layer must be input."

        return network, errMsg

    def get_RNN_train(self, conf):
        gValue = gVal()
        errMsg = "S"
        outFlag = "N"
        matrix = conf.data.matrix

        learnrate = conf.data.learnrate
        num_layers = len(conf.layer)

        for i in range(0, int(num_layers)):
            data = conf.layer[i]
            if (data.type == "input"):
                network = input_data(shape=[None, matrix[0], matrix[1]], name='input')
            elif (data.type == "rnn"):
                if gValue.log == "Y":
                    print("get_RNN_train Clear.........."+str(data.type))

                network = tflearn.lstm(network, 512, return_seq=True)
                network = tflearn.lstm(network, 512)
            elif (data.type == "out"):
                if gValue.log == "Y":
                    print("get_RNN_train Clear.........." + str(data.type))
                network = fully_connected(network, conf.data.y_shape[1], activation=str(data.active))
                network = regression(network, optimizer='adam', learning_rate=learnrate,
                                     loss='categorical_crossentropy', name='target')
                outFlag = "Y"


        if outFlag == "N":
            errMsg = "Error[000003]: Out Layer must be input."


        return network, errMsg