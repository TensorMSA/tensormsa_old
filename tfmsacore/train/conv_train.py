# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tflearn as tflearn

from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
from tfmsacore.data import json_conv, json_loader
from tfmsacore.utils import checker
from tfmsacore.netconf import nn_config_manager
import tensorflow as tf
from tfmsacore.models import nn_data_manager
import numpy as np



def train_conv_network(nn_id):
    """
    Train Convolutional Neural Network and save all result on data base
    :param nn_id:
    :return:
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
        TO-DO : load train data from spark
        """
        # data_set = json_conv.JsonDataConverter().convert_json_to_matrix(json_loader.load_data(nn_id))
        train_x = np.array(json_loader.load_data(nn_id) , np.float32)
        train_y = np.array(json_loader.load_tag(nn_id), np.float32)
        test_x = np.array(json_loader.load_data(nn_id), np.float32)
        test_y = np.array(json_loader.load_tag(nn_id), np.float32)

        """
        TO-DO : setting data and variable
        """
        datalen = conf.data.datalen
        taglen = conf.data.taglen
        matrix = conf.data.matrix
        learnrate = conf.data.learnrate
        train_x = np.reshape(train_x, (-1, matrix[0],matrix[1], 1))
        test_x = np.reshape(test_x, (-1, matrix[0], matrix[1], 1))

        """
        TO-DO : rebuild configuration
        """
        # create network conifg
        num_layers = len(conf.layer)
        for i in range(0, num_layers):

            data = conf.layer[i]
            print(data.active)
            if(data.type == "input"):
                network = input_data(shape=[None, matrix[0], matrix[1], 1], name='input')
                network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active), regularizer=data.regualizer)
                network = max_pool_2d(network, data.maxpoolmatrix)
                network = local_response_normalization(network)

            elif (data.type == "cnn"):
                network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active), regularizer=data.regualizer)
                network = max_pool_2d(network, data.maxpoolmatrix)
                network = local_response_normalization(network)

            elif(data.type == "drop"):
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

        """
        TO-DO : restore trained data
        """
        nn_data_manager.load_trained_data(nn_id, network)

        """
        TO-DO : run model (spark also need to be considered)
        """
        # Training
        model = tflearn.DNN(network, tensorboard_verbose=0)
        model.fit({'input': train_x}, {'target': train_y}, n_epoch=5,
                  validation_set=({'input': test_x}, {'target': test_y}),
                  snapshot_step=100, show_metric=True, run_id='convnet_mnist')

        """
        TO-DO : save trained data
        """
        nn_data_manager.save_trained_data(nn_id, network)

        return "success"

    except SyntaxError as e :
        return e

#for test purpose
#train_conv_network("sample")