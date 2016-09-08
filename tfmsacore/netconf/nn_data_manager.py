# -*- coding: utf-8 -*-

import json
import os
import tensorflow as tf

def load_trained_data(nn_id, session):
    """
    Load Net Trained Weights and Bias from data base
    :param nn_id:
    :return:
    """

    directory = "/tensorMSA/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(directory + nn_id + ".ckpt"):
        saver = tf.train.Saver()
        saver.restore(session, directory + nn_id + ".ckpt")

    print("load model completed for [ " + nn_id + "]")
    """
    TO-DO : get data from postgresql db and load it on the model
    """
    return session


def save_trained_data(nn_id, session):
    """
    Load Net Trained Weights and Bias from data base
    :param nn_id:
    :return:
    """
    directory = "/tensorMSA/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    saver = tf.train.Saver()
    save_path = saver.save(session, directory + nn_id + ".ckpt")
    print ("Model saved in file: ", save_path)

    print("save model completed for [ " + nn_id + "]")
    """
    TO-DO : save trained data on the data base
    """
    return session
