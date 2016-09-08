# -*- coding: utf-8 -*-

import json
import os
import tensorflow as tf

def load_trained_data(nn_id, network):
    """
    Load Net Trained Weights and Bias from data base
    :param nn_id:
    :return:
    """

    print("load model completed for [ " + nn_id + "]")
    """
    TO-DO : get data from postgresql db and load it on the model
    """
    return network


def save_trained_data(nn_id, network):
    """
    Load Net Trained Weights and Bias from data base
    :param nn_id:
    :return:
    """

    print("save model completed for [ " + nn_id + "]")
    """
    TO-DO : save trained data on the data base
    """
    return network