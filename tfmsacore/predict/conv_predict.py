# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import json

import numpy as np

import tflearn as tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
from tfmsacore.netconf import nn_config_manager, nn_data_manager
from tfmsacore.utils import checker

def predict_conv_network(nn_id , req_data):
    """
        Predict Convolutional Neural Network and save all result on data base
        :param nn_id : neural network id
        :param req_data : test request data
        :return: predict result in array
        """

    try :
        """
        TO-DO : check request nn id, conf, data and other setting are ok
        """
        check_result = checker.check_requested_nn(nn_id)
        if(check_result != "ok"):
            raise SyntaxError(check_result)

        """
        TO-DO : load NN conf form db
        """
        conf = nn_config_manager.load_conf(nn_id)

        """
        TO-DO : setting data and variable
        """
        datalen = conf.data.datalen
        taglen = conf.data.taglen
        matrix = conf.data.matrix
        learnrate = conf.data.learnrate
        request_x = np.reshape(json.loads(req_data), (-1, matrix[0], matrix[1],1))


        """
        TO-DO : rebuild configuration
        """
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

        # set to real tensorflow
        model = tflearn.DNN(network, tensorboard_verbose=0)

        """
        TO-DO : restore trained data
        """
        model = nn_data_manager.load_trained_data(nn_id, model)
        result = model.predict(request_x)

        return result

    except SyntaxError as e :
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