# import numpy as np
# import tflearn
# from tflearn.datasets import titanic
# from tflearn.data_utils import load_csv
import tensorflow as tf
# import json
# import codecs
# # json utils
# from __future__ import division, print_function, absolute_import
import numpy as np
import tflearn as tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
# from tfmsacore import data as td
# from tfmsacore import netconf
# from tfmsacore import utils
# from tfmsacore.utils import JsonDataConverter,CusJsonEncoder
import json, math

class gVal:
    log = "Y"

class JsonObject:

    def __init__(self, d):
        self.__dict__ = d

    def __getitem__(self, item):
        return self.__dict__[item]

    def keys(self):
        return self.__dict__.keys()

    def get_dict(self):
        return self.__dict__

    def dumps(self):
        # only for the simple
        return self.__dict__

# Preprocessing function
def preprocess(detailData, to_ignore, to_outtag):
    tmpData = []
    headerData = []
    # print(range(len(detailData)))
    for i in range(len(detailData)):
        for j in range(len(to_outtag)):
            tmpData.append(detailData[i][to_outtag[j]])
        headerData.append(tmpData)
        tmpData = []

    to_ignore = to_ignore+to_outtag

    for id in sorted(to_ignore, reverse=True):
        [r.pop(id) for r in detailData]

    train_x = np.array(detailData, np.float32)
    train_y = np.array(headerData, np.float32)

    print("train_x=", train_x)
    print("train_y=", train_y)

    return train_x, train_y



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
                    errMsg = "Error[000002]: Filter must be larger than [2, 2] Filter:[" + str(ft.cnnfilter) + "," + str(ft.cnnfilter) + "]"

                if gValue.log == "Y" and errMsg == "S":
                    msg = "check_Filter_MinValue Clear..........len(ft.cnnfilter)="+str(len(ft.cnnfilter))+"  ft.cnnfilter="+ str(ft.cnnfilter)
                    print(msg)
        except Exception as e:
            print("Exception check_Filter_MinValue : ", e)
            errMsg = e

        return errMsg

    def check_Filter_Size(self, matrix, cnnfilter):
        try:
            gValue = gVal()
            errMsg = "S"

            if matrix[0] < cnnfilter[0] or matrix[1] < cnnfilter[1]:
                errMsg = "Error[000003]: Filter must not be larger than the input: Filter:[" + str(
                    cnnfilter) + "," + str(cnnfilter) + "] Input: " + str(matrix)

            if gValue.log == "Y" and errMsg == "S":
                msg = "check_Filter_Size Clear..........cnnfilter="+str(cnnfilter)+"  matrix="+ str(matrix)
                print(msg)
        except Exception as e:
            print("Exception check_Filter_Size : ", e)
            errMsg = e

        return errMsg

    def check_Droprate(self, droprate):
        try:
            errMsg = "S"
            print("droprate=",droprate)
            print("droprate=", len(droprate))
            if len(droprate) == 0:
                errMsg = "Error[000002]: Droprate is Null("+str(droprate)+")"

            gValue = gVal()
            if gValue.log == "Y" and errMsg == "S":
                msg = "check_Droprate Clear..........droprate="+str(droprate)
                print(msg)
        except Exception as e:
            print("Exception check_Droprate : ", e)
            errMsg = e

        return errMsg

class NetworkClass:
    def __int__(self):
        self.msg = "Y"

    def get_CNN_train(self, conf):
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
                errMsg = CNNConfCheck().check_Droprate(data.droprate)

                if errMsg == "S":
                    network = fully_connected(network, data.node_in_out[0], activation=str(data.active))
                    network = dropout(network, float(data.droprate))

            elif (data.type == "out"):
                network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
                network = regression(network, optimizer='adam', learning_rate=learnrate,
                                     loss='categorical_crossentropy', name='target')

            elif (data.type == "fully"):
                network = fully_connected(network, data.node_in_out[1], activation=str(data.active))

                # else:
                #     raise SyntaxError("there is no such kind of nn type : " + str(data.active))

        return network, errMsg

def main(case):
    directory = "/home/dev/TensorMSA/tfmsarest/test/"

    net_id = "test"
    confFile = directory + net_id+"_conf.json"
    with open(confFile) as dataFile:
        conf = json.loads(dataFile.read(), object_hook=JsonObject)

    confFile = directory + net_id + "_input.json"
    with open(confFile) as dataFile:
        detailData = json.loads(dataFile.read(), object_hook=JsonObject)[1:]

    # print("data=",detailData)
    #
    # print(type(conf))

    to_ignore = [3, 4]
    to_outtag = [0, 1]
    epoch = 10

    train_x, train_y = preprocess(detailData, to_ignore, to_outtag)
    train_x = np.reshape(train_x, (-1, conf.data.matrix[0], conf.data.matrix[1], 1))
    test_x = train_x
    test_y = train_y

    # # # # Build neural network
    # # net = tflearn.input_data(shape=[None, len(inData[0])])
    # # net = tflearn.fully_connected(net, 32)
    # # net = tflearn.fully_connected(net, 32)
    # # net = tflearn.fully_connected(net, len(outData[0]), activation='softmax')
    # # net = tflearn.regression(net)
    #
    # # # Define model
    # # model = tflearn.DNN(net)
    # #
    # # model.fit(inData, outData, n_epoch=10, batch_size=16, show_metric=True)
    #
    # # # create network conifg
    errMsg = "S"

    if errMsg == "S":
        errMsg = CNNConfCheck().check_Matrix(conf)

    if errMsg == "S":
        errMsg = CNNConfCheck().check_Filter_MinValue(conf)

    if errMsg == "S":
        net, errMsg = NetworkClass().get_CNN_train(conf)


    print("====================================================================")
    print(errMsg)
    print("====================================================================")

    # # Define model
    if errMsg == "S":
        model = tflearn.DNN(net)
        # model.fit(inData, outData, n_epoch=10, batch_size=16, show_metric=True)
        model.fit({'input': train_x}, {'target': train_y}, n_epoch=int(epoch),
                  validation_set=({'input': test_x}, {'target': test_y}),
                  snapshot_step=100, show_metric=True, run_id='convnet_mnist')

if __name__ == '__main__':
    tf.app.run()
