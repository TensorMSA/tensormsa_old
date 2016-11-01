from sklearn import metrics
import tensorflow as tf
from tensorflow.contrib import learn
import numpy as np
from tfmsacore import netconf
from tfmsacore import utils
from TensorMSA import const
import json, math
from tfmsacore.netcommon.conv_common import ConvCommonManager


def train_conv_network(nn_id, epoch = 100, testset = 100):
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
            train_data_set, train_label_set = ConvCommonManager().prepare_image_data(nn_id, net_info, conf_info)
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
        test_x = np.array(train_data_set, np.float32)
        test_y = np.array(train_label_set, np.float32)

        # strucut layer
        utils.tfmsa_logger("[5]struct cnn layer")
        network = ConvCommonManager().struct_cnn_layer(conf_info, train_data_set, train_label_set)

        # define classifier
        utils.tfmsa_logger("[6]define classifier")
        classifier = learn.TensorFlowEstimator(
            model_fn=network,
            n_classes=n_class,
            batch_size=100,
            steps=int(epoch),
            learning_rate=learnrate)

        # load model
        utils.tfmsa_logger("[7]load trained model")
        netconf.nn_model_manager.load_trained_data(nn_id, classifier)

        # start train
        utils.tfmsa_logger("[8]start train")
        classifier.fit(train_x, train_y)

        # save model
        utils.tfmsa_logger("[9]save trained model")
        netconf.nn_model_manager.save_trained_data(nn_id, classifier)

        # accuracy test
        utils.tfmsa_logger("[10]accuracy test")
        score = metrics.accuracy_score(
            test_y, classifier.predict(test_x))
        print('Accuracy: {0:f}'.format(score))

        return format(score)

    except Exception as e:
        print("Error Message : {0}".format(e))
        raise Exception(e)