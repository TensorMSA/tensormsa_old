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



def spark_train_conv_network(nn_id):
    """
    Train Convolutional Neural Network and save all result on data base
    :param nn_id:
    :return:
    """

    try :
        print("on development now sorry")

        return "on development now sorry"

    except SyntaxError as e :
        return e

