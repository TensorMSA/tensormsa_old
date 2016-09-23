# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import numpy as np
import tflearn as tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
from tfmsacore import data as td
from tfmsacore import netconf
from tfmsacore import utils
from tfmsacore.utils import tfmsa_logger


def predict_conv_network(nn_id , req_data):
    """
        Predict Convolutional Neural Network and save all result on data base
        :param nn_id : neural network id
        :param req_data : test request data
        :return: predict result in array
        """

    try :
        tfmsa_logger("start prediction....")

        # check network is ready to predict
        utils.check_requested_nn(nn_id)

        # load NN conf form db
        conf = netconf.load_conf(nn_id)

        # modify predict fit to tarin
        sp_loader = td.SparkLoader().get_predict_data(nn_id, req_data)

        # set spaces for input data
        datalen = conf.data.datalen
        matrix = conf.data.matrix
        learnrate = conf.data.learnrate
        request_x = np.reshape(sp_loader.m_train, (-1, matrix[0], matrix[1],1))

        # create network conifg
        num_layers = len(conf.layer)
        for i in range(0, num_layers):

            data = conf.layer[i]
            if(data.type == "input"):
                network = input_data(shape=[None, matrix[0], matrix[1],1], name='input')
                network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active), regularizer=data.regualizer)
                network = max_pool_2d(network, data.maxpoolmatrix)
                network = local_response_normalization(network)

            elif (data.type == "cnn"):
                network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active), regularizer=data.regualizer)
                network = max_pool_2d(network, data.maxpoolmatrix)
                network = local_response_normalization(network)

            elif(data.type == "drop"):
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

            else :
                raise SyntaxError("there is no such kind of nn type : " + str(data.active))

        # set net conf to real tensorflow
        model = tflearn.DNN(network, tensorboard_verbose=0)

        # restore model and start predict with given data
        model = netconf.nn_data_manager.load_trained_data(nn_id, model)
        result = model.predict(request_x)

        tfmsa_logger("End prediction with result : {0}".format(result))
        return result

    except SyntaxError as e :
        tfmsa_logger("Error while prediction  : {0}".format(e))
        return e



# req_data ="""[ 0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
#                0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
#                0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
#                0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
#                0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
#                0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
#                0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
#                0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ]"""
#
# predict_conv_network("sample" , req_data)