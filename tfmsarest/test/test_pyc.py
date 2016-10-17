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
    # print("detailData=", detailData)
    # print("headerData=", headerData)
    train_x = np.array(detailData, np.float32)
    train_y = np.array(headerData, np.float32)

    print("train_x=", train_x)
    print("train_y=", train_y)

    return train_x, train_y



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


def main(case):
    gValue = gVal()
    errMsg = "S"
    directory = "/home/dev/TensorMSA/tfmsarest/test/"

    net_id = "test"
    confFile = directory + net_id+"_conf.json"
    with open(confFile) as dataFile:
        conf = json.loads(dataFile.read(), object_hook=JsonObject)

    confFile = directory + net_id + "_input.json"
    with open(confFile) as dataFile:
        detailData = json.loads(dataFile.read(), object_hook=JsonObject)[1:]

    to_ignore = ""
    to_outtag = ""
    # to_ignore = [3, 4, 8]
    # to_outtag = [0, 1]
    matrix = conf.data.matrix
    learnrate = conf.data.learnrate
    print("matrix",matrix)
    # to_ignore = [2, 3, 4, 6, 7, 11]
    # to_outtag = [0, 1]

    # to_ignore = [3, 4, 6, 7, 11]
    # to_outtag = [0, 1, 2]

    to_ignore = [4, 6, 7, 11]
    to_outtag = [0, 1, 2, 3]

    train_x, train_y = preprocess(detailData, to_ignore, to_outtag)

    ##################################################################################
    conf.data.x_shape = train_x.shape
    conf.data.y_shape = train_y.shape
    ##################################################################################
    # # # create CNN network conifg
    # # # from tfmsacore import validation
    # # # network, errMsg = validation.NetworkClass().get_CNN_traconf.data.x_shapein(conf)

    network, errMsg = NetworkClass().get_CNN_train(conf)
    train_x = np.reshape(train_x, (-1, conf.data.matrix[0], conf.data.matrix[1], 1))

    ##################################################################################
    # # # # create RNN network conifg
    # # # from tfmsacore import validation
    # # # network, errMsg = validation.NetworkClass().get_CNN_traconf.data.x_shapein(conf)

    # network, errMsg = NetworkClass().get_RNN_train(conf)
    # train_x = np.reshape(train_x, (-1, conf.data.matrix[0], conf.data.matrix[1]))

    ##################################################################################


    if gValue.log == "Y":
        print("====================================================================")
        print(errMsg)
        print("====================================================================")

    # # Define model
    if errMsg == "S" or errMsg[0:1] == "W":

        test_x = train_x
        test_y = train_y
        model = tflearn.DNN(network)
        model.fit({'input': train_x}, {'target': train_y}, n_epoch=int(conf.data.epoch),
                  validation_set=({'input': test_x}, {'target': test_y}),
                  snapshot_step=100, show_metric=True, run_id='convnet_mnist')
        acc = model.evaluate(test_x, test_y)
        print(acc)



if __name__ == '__main__':
    tf.app.run()
