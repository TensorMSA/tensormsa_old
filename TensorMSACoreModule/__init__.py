
from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

# 테스트 네트워크 커피규레이션
json_conf = """
                 {
                    "data":
                        {
                             "datalen": 96,
                             "taglen" : 2,
                             "matrix" : [12 , 8]
                        },
                    "layer":
                        [
                            {
                                "seq" : 1,
                                "type" : "cnn",
                                "active" : "relu",
                                "cnnmatrix" : [2,2],
                                "cnnstride" : [1, 1],
                                "maxpoolmatrix" : [2, 2],
                                "maxpoolstride" : [1, 1],
                                "node_in_out" : [1,1]
                            },

                            {
                                "seq" : 2,
                                "type" : "cnn",
                                "active" : "relu",
                                "cnnmatrix" : [2,2],
                                "cnnstride" : [1, 1],
                                "maxpoolmatrix" : [2, 2],
                                "maxpoolstride" : [1, 1],
                                "node_in_out" : [1,32]
                            },

                            {
                                "seq" : 3,
                                "type" : "drop",
                                "active" : "relu",
                                "cnnmatrix" : "",
                                "cnnstride" : "",
                                "maxpoolmatrix" : "",
                                "maxpoolstride" : "",
                                "node_in_out" : [192,100]
                            },
                            {
                                "seq" : 4,
                                "type" : "out",
                                "active" : "softmax",
                                "cnnmatrix" : "",
                                "cnnstride" : "",
                                "maxpoolmatrix" : "",
                                "maxpoolstride" : "",
                                "node_in_out" : [100,2]
                            }
                        ]
                 }

             """

# Data loading and preprocessing
import tflearn.datasets.mnist as mnist
X, Y, testX, testY = mnist.load_data(one_hot=True)
X = X.reshape([-1, 28, 28, 1])
testX = testX.reshape([-1, 28, 28, 1])

# Building convolutional network
network = input_data(shape=[None, 28, 28, 1], name='input')
network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = fully_connected(network, 128, activation='tanh')
network = dropout(network, 0.8)
network = fully_connected(network, 256, activation='tanh')
network = dropout(network, 0.8)
network = fully_connected(network, 10, activation='softmax')
network = regression(network, optimizer='adam', learning_rate=0.01,
                     loss='categorical_crossentropy', name='target')

# Training
model = tflearn.DNN(network, tensorboard_verbose=0)
model.fit({'input': X}, {'target': Y}, n_epoch=20,
           validation_set=({'input': testX}, {'target': testY}),
           snapshot_step=100, show_metric=True, run_id='convnet_mnist')
