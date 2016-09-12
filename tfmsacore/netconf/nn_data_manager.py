# -*- coding: utf-8 -*-

import json
import os
import tensorflow as tf

def load_trained_data(nn_id, model):
    """
    Load Net Trained Weights and Bias from data base
    :param nn_id:
    :return:
    """
    directory = "/tensorMSA/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(directory + nn_id + ".ckpt"):
        model.load(directory + nn_id + ".ckpt")


    print("load model completed for [ " + nn_id + "]")
    """
    TO-DO : get data from postgresql db and load it on the model
    """
    return model


def save_trained_data(nn_id, model):
    """
    Load Net Trained Weights and Bias from data base
    :param nn_id:
    :return:
    """

    print(type(model))
    directory = "/tensorMSA/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    model.save(directory + nn_id + ".ckpt")

    print("save model completed for [ " + nn_id + "]")
    """
    TO-DO : save trained data on the data base
    """
    return model
