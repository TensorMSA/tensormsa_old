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



def train_conv_network(nn_id, epoch, testset):
    """
    Train Convolutional Neural Network and save all result on data base
    :param nn_id:
    :return:
    """

    try :
        """
        TO-DO : check request nn id, conf, data and other setting are ok
        """
        utils.check_requested_nn(nn_id)

        # load NN conf form db
        conf = netconf.load_conf(nn_id)

        """
        TO-DO : need to get data form spark
        TO-DO : need to sample the test set
        """
        # data_set = json_conv.JsonDataConverter().convert_json_to_matrix(json_loader.load_data(nn_id))
        train_x = np.array(td.SparkLoader.get_train_data(nn_id) , np.float32)
        train_y = np.array(td.SparkLoader.get_train_data(nn_id), np.float32)
        test_x = np.array(td.SparkLoader.get_train_data(nn_id), np.float32)
        test_y = np.array(td.SparkLoader.get_train_data(nn_id), np.float32)

        """
        TO-DO : need to get data form spark
        """
        datalen = conf.data.datalen
        taglen = conf.data.taglen
        matrix = conf.data.matrix
        learnrate = conf.data.learnrate
        train_x = np.reshape(train_x, (-1, matrix[0],matrix[1],1))
        test_x = np.reshape(test_x, (-1, matrix[0], matrix[1],1))

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

        #load network
        model = netconf.nn_data_manager.load_trained_data(nn_id, model)

        #train network
        model.fit({'input': train_x}, {'target': train_y}, n_epoch=epoch,
                  validation_set=({'input': test_x}, {'target': test_y}),
                  snapshot_step=100, show_metric=True, run_id='convnet_mnist')

        # save trained network
        netconf.nn_data_manager.save_trained_data(nn_id, model)

        # save train statistics result
        acc = model.evaluate(test_x, test_y)
        netconf.nn_common_manager.set_train_result(nn_id, acc)

        return acc

    except Exception as e :
        raise Exception(e)

#for test purpose
#train_conv_network("sample")