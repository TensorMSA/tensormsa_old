# -*- coding: utf-8 -*-
import os
import shutil
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings

def chk_trained_data(net_id):
    """
    check if trained data exist with net_id
    :param net_id: neural network id
    :return:
    """
    directory = settings.HDFS_MODEL_ROOT + "/" + net_id + "/"
    net_id = net_id + "_model.ckpt"

    try:
        if os.path.isfile(directory +  "/"  + net_id):
            if(os.stat(directory + "/"  + net_id).st_size == 0):
                return False
            else:
                return True
        else :
            return False
    except :
        return False


def load_trained_data(nn_id, model):
    """
    Load Net Trained Weights and Bias from data base
    :param nn_id: neural network id
    :param mdoe : tflearn model
    :return:tflearn model
    """
    directory = settings.HDFS_MODEL_ROOT + "/" + nn_id + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(directory + "/" + nn_id + "_model.ckpt"):
        model.load(directory + "/" +  nn_id + "_model.ckpt")

    return model


def save_trained_data(nn_id, model):
    """
    Load Net Trained Weights and Bias from data base
    :param nn_id: neural network id
    :param mdoe : tflearn model
    :return:tflearn model
    """

    directory = settings.HDFS_MODEL_ROOT + "/" + nn_id + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    model.save(directory + "/"  + nn_id + "_model.ckpt")
    tfmsa_logger("save model completed for ")

    return model


def remove_trained_data(nn_id):
    """
    remove Net Trained Weights and Bias from data base
    :param nn_id: neural network id
    :param mdoe : tflearn model
    :return:tflearn model
    """

    try:
        directory = settings.HDFS_MODEL_ROOT + "/" + nn_id + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.isfile(directory + "/" + nn_id + "_model.ckpt"):
            os.remove(directory + "/" + nn_id + "_model.ckpt")
            os.remove(directory + "/" + nn_id + "_model.ckpt.meta")
            tfmsa_logger("remove model completed for [ " + nn_id + "]")
    except Exception as e:
        tfmsa_logger("remove trained error : {0}".format(e))