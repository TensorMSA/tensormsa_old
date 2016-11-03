from sklearn import metrics
import tensorflow as tf
from tensorflow.contrib import learn
import numpy as np
from tfmsacore import netconf
from tfmsacore import utils
from TensorMSA import const
import json, math
from tfmsacore.netcommon.conv_common import ConvCommonManager


def predict_conv_network(nn_id, epoch = 100, testset = 100):
    try:
        # check network is ready to train
        utils.tfmsa_logger("[1]check pre steps ready")
        utils.check_requested_nn(nn_id)

        # get network base info
        utils.tfmsa_logger("[2]get network base info")
        net_info = netconf.get_network_config(nn_id)

        # get network format info
        utils.tfmsa_logger("[3]get network format info")
        conf_info = netconf.load_conf(nn_id)

        # load train data
        utils.tfmsa_logger("[4]load train data")
        train_data_set = []
        train_label_set = []

        if(const.TYPE_IMAGE == net_info['preprocess']):
            train_data_set, train_label_set = ConvCommonManager(conf_info).prepare_image_data(nn_id, net_info)
        elif(const.TYPE_DATA_FRAME == net_info['preprocess']):
            raise Exception("function not ready")
        elif(const.TYPE_TEXT == net_info['preprocess']):
            raise Exception("function not ready")
        else:
            raise Exception("unknown data type")

        learnrate = conf_info.data.learnrate
        n_class = len(json.loads(net_info['datasets']))
        train_x = np.array(train_data_set, np.float32)
        train_y = np.array(train_label_set, np.float32)

        # define classifier
        utils.tfmsa_logger("[5]define classifier")
        classifier = learn.TensorFlowEstimator(
            model_fn=ConvCommonManager(conf_info).struct_cnn_layer,
            n_classes=n_class,
            batch_size=100,
            steps=int(epoch),
            learning_rate=learnrate)

        # load model
        utils.tfmsa_logger("[6]load trained model")
        netconf.nn_model_manager.load_trained_data(nn_id, classifier)

        # start train
        utils.tfmsa_logger("[7]start train")
        classifier.fit(train_x, train_y)

        # save model
        utils.tfmsa_logger("[8]save trained model")
        netconf.nn_model_manager.save_trained_data(nn_id, classifier)

        return len(train_y)

    except Exception as e:
        print("Error Message : {0}".format(e))
        raise Exception(e)