from sklearn import metrics
import tensorflow as tf
from tensorflow.contrib import learn
import numpy as np
from tfmsacore.data.image_manager import ImageManager
from tfmsacore import netconf
from tfmsacore import utils
from tfmsacore.utils import JsonDataConverter,CusJsonEncoder
import json, math
from tfmsacore import preprocess

def train_conv_network(nn_id, epoch = 100, testset = 100):
    try:
        # check network is ready to train
        utils.tfmsa_logger("[1]check pre steps ready")
        utils.check_requested_nn(nn_id)

        # get network base info
        utils.tfmsa_logger("[2]get network base info")
        net_info = netconf.get_network_config(nn_id)

        # get data format info
        utils.tfmsa_logger("[3]get network format info")
        format_info = netconf.load_ori_format(nn_id)

        # check current data pointer
        """
        TO-DO : case when data size is big
        """

        # get train data from HDFS
        utils.tfmsa_logger("[4]load data from hdfs")
        row_data_arr = ImageManager().load_data(net_info['dir'], net_info['table'], "0", "10")

        utils.tfmsa_logger("[5]convert image to array")
        train_data_set = []
        for row_data in row_data_arr:
            arr = preprocess.ImagePreprocess().resize_bytes_image(row_data['bt'], format_info['x_size'], format_info['y_size'])
            train_data_set.append(arr)

        print(train_data_set)

    except Exception as e:
        print("Error Message : {0}".format(e))
        raise Exception(e)

#
#         # change conf info
#         utils.tfmsa_logger("[3]save recalculated data info")
#         save_changed_data_info(nn_id, sp_loader)
#
#         # load NN conf form db
#         utils.tfmsa_logger("[4]load net conf form db")
#         conf = netconf.load_format(nn_id)
#
#         # set train and evaluation data
#         utils.tfmsa_logger("[5]set tensor variables")
#         train_x = np.array(sp_loader.m_train, np.float32)
#         train_y = np.array(sp_loader.m_tag, np.float32)
#         test_x = np.array(sp_loader.m_train, np.float32)
#         test_y = np.array(sp_loader.m_tag, np.float32)
#
#         # set data parmas
#         datalen = conf.data.datalen
#         taglen = conf.data.taglen
#         matrix = conf.data.matrix
#         learnrate = conf.data.learnrate
#         train_x = np.reshape(train_x, (-1, matrix[0], matrix[1], 1))
#         test_x = np.reshape(test_x, (-1, matrix[0], matrix[1], 1))
#
#         # create network conifg
#         utils.tfmsa_logger("[6]set networks on tflearn")
#         num_layers = len(conf.layer)
#
#         for i in range(0, int(num_layers)):
#
#             data = conf.layer[i]
#
#             if (data.type == "input"):
#                 network = input_data(shape=[None, matrix[0], matrix[1], 1], name='input')
#                 network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active),
#                                   regularizer=data.regualizer)
#                 network = max_pool_2d(network, data.maxpoolmatrix)
#                 network = local_response_normalization(network)
#
#             elif (data.type == "cnn"):
#                 network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active),
#                                   regularizer=data.regualizer)
#                 network = max_pool_2d(network, data.maxpoolmatrix)
#                 network = local_response_normalization(network)
#
#             elif (data.type == "drop"):
#                 network = fully_connected(network, data.node_in_out[0], activation=str(data.active))
#                 network = dropout(network, int(data.droprate))
#                 network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
#                 network = dropout(network, int(data.droprate))
#
#             elif (data.type == "out"):
#                 network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
#                 network = regression(network, optimizer='adam', learning_rate=learnrate,
#                                      loss='categorical_crossentropy', name='target')
#
#             elif (data.type == "fully"):
#                 network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
#
#             else:
#                 raise SyntaxError("there is no such kind of nn type : " + str(data.active))
#
#         # set to real tensorflow
#         utils.tfmsa_logger("[7]set net conf on real tensorflow")
#         model = tflearn.DNN(network, tensorboard_verbose=0)
#
#         # load network
#         utils.tfmsa_logger("[8]load pretrained model")
#         model = netconf.nn_data_manager.load_trained_data(nn_id, model)
#
#         # train network
#         utils.tfmsa_logger("[9]Start Train")
#         model.fit({'input': train_x}, {'target': train_y}, n_epoch=int(epoch),
#                   validation_set=({'input': test_x}, {'target': test_y}),
#                   snapshot_step=100, show_metric=True, run_id='convnet_mnist')
#
#         # save trained network
#         utils.tfmsa_logger("[10]save trained model")
#         netconf.nn_data_manager.save_trained_data(nn_id, model)
#
#         # save train statistics result
#         utils.tfmsa_logger("[11]evaluation accuracy and save")
#         acc = model.evaluate(test_x, test_y)
#         netconf.nn_common_manager.set_train_result(nn_id, round(acc, 3))
#
#         return acc
#



#
#
# def max_pool_2x2(tensor_in):
#     return tf.nn.max_pool(
#         tensor_in, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
#
#
# def conv_model(X, y):
#     # pylint: disable=invalid-name,missing-docstring
#     # reshape X to 4d tensor with 2nd and 3rd dimensions being image width and
#     # height final dimension being the number of color channels.
#     X = tf.reshape(X, [-1, 28, 28, 1])
#     # first conv layer will compute 32 features for each 5x5 patch
#     with tf.variable_scope('conv_layer1'):
#         h_conv1 = learn.ops.conv2d(X, n_filters=32, filter_shape=[5, 5],
#                                    bias=True, activation=tf.nn.relu)
#         h_pool1 = max_pool_2x2(h_conv1)
#     # second conv layer will compute 64 features for each 5x5 patch.
#     with tf.variable_scope('conv_layer2'):
#         h_conv2 = learn.ops.conv2d(h_pool1, n_filters=64, filter_shape=[5, 5],
#                                    bias=True, activation=tf.nn.relu)
#         h_pool2 = max_pool_2x2(h_conv2)
#         # reshape tensor into a batch of vectors
#         h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
#   # densely connected layer with 1024 neurons.
#     h_fc1 = tf.contrib.layers.dropout(
#         tf.contrib.layers.legacy_fully_connected(
#             h_pool2_flat, 1024, weight_init=None, activation_fn=tf.nn.relu))
#     return learn.models.logistic_regression(h_fc1, y)
#
# # Training and predicting.
# classifier = learn.TensorFlowEstimator(
#     model_fn=conv_model, n_classes=10, batch_size=100, steps=20000,
#     learning_rate=0.001)
# classifier.fit(mnist.train.images, mnist.train.labels)
# score = metrics.accuracy_score(
#     mnist.test.labels, classifier.predict(mnist.test.images))
# print('Accuracy: {0:f}'.format(score))





# # -*- coding: utf-8 -*-
# from __future__ import division, print_function, absolute_import
# import numpy as np
# import tflearn as tflearn
# from tflearn.layers.conv import conv_2d, max_pool_2d
# from tflearn.layers.core import input_data, dropout, fully_connected
# from tflearn.layers.estimator import regression
# from tflearn.layers.normalization import local_response_normalization
# from tfmsacore import data as td
# from tfmsacore import netconf
# from tfmsacore import utils
# from tfmsacore.utils import JsonDataConverter,CusJsonEncoder
# import json, math
#
#
#
#
# def save_changed_data_info(nn_id, spark_loader):
#     """
#     save train data size related information on db
#     :param nn_id: neural network management id
#     :param spark_loader: spark_loader class object
#     :return: None
#     """
#
#     json_conf = netconf.load_conf(nn_id)
#     json_conf.data.datalen = spark_loader.train_len
#     json_conf.data.taglen = spark_loader.tag_len
#     len_sqrt = int(math.ceil(math.sqrt(int(spark_loader.train_len))))
#
#     flag = False
#
#     for i in range(0, len_sqrt):
#         for x in range(0, len_sqrt):
#             if(int(json_conf.data.datalen) == (len_sqrt + x) * (len_sqrt - i)):
#                 json_conf.data.matrix = [(len_sqrt + x), len_sqrt - i]
#                 flag = True
#
#     if(flag == False):
#         json_conf.data.matrix = [spark_loader.train_len, 1]
#
#     netconf.save_conf(nn_id, json.dumps(json_conf, cls=CusJsonEncoder))
#
#
# def train_conv_network(nn_id, epoch, testset):
#     """
#     Train Convolutional Neural Network and save all result on data base
#     :param nn_id:
#     :return:
#     """
#
#     try :
#         # check network is ready to train
#         utils.tfmsa_logger("[1]check request nn data")
#         utils.check_requested_nn(nn_id)
#
#         # get train data from spark
#         utils.tfmsa_logger("[2]get data from spark")
#         sp_loader = td.DFPreProcessor().get_train_data(nn_id)
#
#         # change conf info
#         utils.tfmsa_logger("[3]save recalculated data info")
#         save_changed_data_info(nn_id, sp_loader)
#
#         # load NN conf form db
#         utils.tfmsa_logger("[4]load net conf form db")
#         conf = netconf.load_conf(nn_id)
#
#         # set train and evaluation data
#         utils.tfmsa_logger("[5]set tensor variables")
#         train_x = np.array(sp_loader.m_train , np.float32)
#         train_y = np.array(sp_loader.m_tag , np.float32)
#         test_x = np.array(sp_loader.m_train, np.float32)
#         test_y = np.array(sp_loader.m_tag, np.float32)
#
#         # set data parmas
#         datalen = conf.data.datalen
#         taglen = conf.data.taglen
#         matrix = conf.data.matrix
#         learnrate = conf.data.learnrate
#         train_x = np.reshape(train_x, (-1, matrix[0],matrix[1],1))
#         test_x = np.reshape(test_x, (-1, matrix[0], matrix[1],1))
#
#         # create network conifg
#         utils.tfmsa_logger("[6]set networks on tflearn")
#         num_layers = len(conf.layer)
#         for i in range(0, int(num_layers)):
#
#             data = conf.layer[i]
#
#             if(data.type == "input"):
#                 network = input_data(shape=[None, matrix[0], matrix[1],1], name='input')
#                 network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active), regularizer=data.regualizer)
#                 network = max_pool_2d(network, data.maxpoolmatrix)
#                 network = local_response_normalization(network)
#
#             elif (data.type == "cnn"):
#                 network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active), regularizer=data.regualizer)
#                 network = max_pool_2d(network, data.maxpoolmatrix)
#                 network = local_response_normalization(network)
#
#             elif(data.type == "drop"):
#                 network = fully_connected(network, data.node_in_out[0], activation=str(data.active))
#                 network = dropout(network, int(data.droprate))
#                 network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
#                 network = dropout(network, int(data.droprate))
#
#             elif (data.type == "out"):
#                 network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
#                 network = regression(network, optimizer='adam', learning_rate=learnrate,
#                                      loss='categorical_crossentropy', name='target')
#
#             elif (data.type == "fully"):
#                 network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
#
#             else :
#                 raise SyntaxError("there is no such kind of nn type : " + str(data.active))
#
#         # set to real tensorflow
#         utils.tfmsa_logger("[7]set net conf on real tensorflow")
#         model = tflearn.DNN(network, tensorboard_verbose=0)
#
#         #load network
#         utils.tfmsa_logger("[8]load pretrained model")
#         model = netconf.nn_data_manager.load_trained_data(nn_id, model)
#
#         #train network
#         utils.tfmsa_logger("[9]Start Train")
#         model.fit({'input': train_x}, {'target': train_y}, n_epoch=int(epoch),
#                   validation_set=({'input': test_x}, {'target': test_y}),
#                   snapshot_step=100, show_metric=True, run_id='convnet_mnist')
#
#         # save trained network
#         utils.tfmsa_logger("[10]save trained model")
#         netconf.nn_data_manager.save_trained_data(nn_id, model)
#
#         # save train statistics result
#         utils.tfmsa_logger("[11]evaluation accuracy and save")
#         acc = model.evaluate(test_x, test_y)
#         netconf.nn_common_manager.set_train_result(nn_id, round(acc, 3))
#
#         return acc
#
#     except Exception as e :
#         print ("Error Message : {0}".format(e))
#         raise Exception(e)
#
# #for evaluation purpose
# #train_conv_network("sample")