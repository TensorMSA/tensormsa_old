# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tflearn as tflearn

from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
from tfmsacore.data import json_conv, json_loader
from tfmsacore.utils import checker
from tfmsacore.netconf import config_manager







"""
TO-DO : start train with spark data
"""

"""
TO-DO : save trained data
"""

"""
TO-DO : save trained data
"""

def train_conv_network(nn_id):
    """
    train requested nn
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
        conf = config_manager.load_conf(nn_id)

        """
        TO-DO : load train data from spark
        """
        data_set = json_conv.JsonDataConverter().convert_json_to_matrix(json_loader.load_data(nn_id))

        """
        TO-DO : rebuild model with conf data
        """
        # "type": "cnn",
        # "active": "relu",
        # "cnnmatrix": [2, 2],
        # "cnnstride": [1, 1],
        # "maxpoolmatrix": [2, 2],
        # "maxpoolstride": [1, 1],
        # "node_in_out": [1, 1],
        # "regualizer": "",
        # "padding": "SAME"
        num_layers = len(conf.layer)
        for i in range(0, num_layers):

            if(conf.layer[0].type == "cnn"):
                network = input_data(shape=[None, 28, 28, 1], name='input')
                network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
                network = max_pool_2d(network, 2)
                network = local_response_normalization(network)

            elif(conf.layer[0].type == "drop"):
                network = input_data(shape=[None, 28, 28, 1], name='input')
                network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
                network = max_pool_2d(network, 2)
                network = local_response_normalization(network)


    except SyntaxError as e :
        return e

#
#
# X, Y, testX, testY = json_converter.load_data(one_hot=True)
# X = X.reshape([-1, 28, 28, 1])
# testX = testX.reshape([-1, 28, 28, 1])
#
# # Building convolutional network
# network = input_data(shape=[None, 28, 28, 1], name='input')
# network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
# network = max_pool_2d(network, 2)
# network = local_response_normalization(network)
# network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
# network = max_pool_2d(network, 2)
# network = local_response_normalization(network)
# network = fully_connected(network, 128, activation='tanh')
# network = dropout(network, 0.8)
# network = fully_connected(network, 256, activation='tanh')
# network = dropout(network, 0.8)
# network = fully_connected(network, 10, activation='softmax')
# network = regression(network, optimizer='adam', learning_rate=0.01,
#                      loss='categorical_crossentropy', name='target')
#
# # Training
# model = tflearn.DNN(network, tensorboard_verbose=0)
# model.fit({'input': X}, {'target': Y}, n_epoch=20,
#            validation_set=({'input': testX}, {'target': testY}),
#            snapshot_step=100, show_metric=True, run_id='convnet_mnist')
#
#

train_conv_network("sample")