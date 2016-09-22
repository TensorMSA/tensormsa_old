# -*- coding: utf-8 -*-
import os
import shutil


def chk_trained_data(net_id):
    """
    check if trained data exist with net_id
    :param net_id: neural network id
    :return:
    """
    directory = "/tensorMSA/data/"
    net_id = net_id + ".ckpt"

    try:
        if os.path.isfile(directory + net_id):
            if(os.stat(directory + net_id).st_size == 0):
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
    directory = "/tensorMSA/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(directory + nn_id + ".ckpt"):
        model.load(directory + nn_id + ".ckpt")
        print("load model completed for [ " + nn_id + "]")

    return model


def save_trained_data(nn_id, model):
    """
    Load Net Trained Weights and Bias from data base
    :param nn_id: neural network id
    :param mdoe : tflearn model
    :return:tflearn model
    """

    directory = "/tensorMSA/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    model.save(directory + nn_id + ".ckpt")

    print("save model completed for [ " + nn_id + "]")
    """
    TO-DO : save trained data on the data base
    """
    return model


def remove_trained_data(nn_id, model):
    """
    remove Net Trained Weights and Bias from data base
    :param nn_id: neural network id
    :param mdoe : tflearn model
    :return:tflearn model
    """
    directory = "/tensorMSA/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(directory + nn_id + ".ckpt"):
        os.remove(directory + nn_id + ".ckpt")
        print("remove model completed for [ " + nn_id + "]")

    return model


def test_data_move():
    """
    only for the test purpose
    :return:
    """
    to_path = "/tensorMSA/data/"
    #from_path = os.path.dirname(os.path.realpath(__file__))
    from_path = os.path.dirname(os.getcwd() +"/tfmsacore/data/")
    shutil.copy(os.path.join(from_path, "sample_conf.json"), to_path)
    shutil.copy(os.path.join(from_path, "sample_data.json"), to_path)
    shutil.copy(os.path.join(from_path, "sample_tag.json"), to_path)