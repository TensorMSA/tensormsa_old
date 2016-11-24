from sklearn import metrics
import tensorflow as tf
from tensorflow.contrib import learn
import numpy as np
from tfmsacore import netconf
from tfmsacore import utils
from TensorMSA import const
import json, math
from tfmsacore.netcommon.conv_common import ConvCommonManager
from tfmsacore.netcommon import monitors_common as Monitors


def train_conv_network(nn_id, epoch=1000, testset=100):
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

        if (const.TYPE_IMAGE == net_info['preprocess']):
            train_data_set, train_label_set = ConvCommonManager(conf_info).prepare_image_data(nn_id, net_info)
        elif (const.TYPE_DATA_FRAME == net_info['preprocess']):
            raise Exception("function not ready")
        elif (const.TYPE_TEXT == net_info['preprocess']):
            raise Exception("function not ready")
        else:
            raise Exception("unknown data type")

        # data size info change
        utils.tfmsa_logger("[5]modify data stuctor info")
        # ConvCommonManager(conf_info).save_changed_data_info(nn_id, train_data_set)

        learnrate = conf_info.data.learnrate
        conf_info.n_class = len(json.loads(net_info['datasets']))

        # change to nummpy array
        train_x = np.array(np.array(train_data_set).astype(float), np.float32)
        train_y = np.array(train_label_set, np.int32)

        # define classifier
        utils.tfmsa_logger("[6]define classifier")
        classifier = learn.Estimator(model_fn=ConvCommonManager(conf_info).struct_cnn_layer,
                                     model_dir=netconf.nn_model_manager.get_model_save_path(nn_id))

        # start train
        utils.tfmsa_logger("[7]fit CNN")
        customsMonitor = Monitors.MonitorCommon(p_nn_id=nn_id, p_max_steps=int(epoch))
        classifier.fit(train_x, train_y, steps=int(epoch), monitors=[customsMonitor])

        return len(train_y)

    except Exception as e:
        print("Error Message : {0}".format(e))
        raise Exception(e)