from sklearn import metrics
import tensorflow as tf
from tensorflow.contrib import learn
import numpy as np
from tfmsacore import netconf
from tfmsacore import utils
from TensorMSA import const
import json, math
from tfmsacore.netcommon.conv_common import ConvCommonManager


def predict_conv_network(nn_id, predict_data):
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

        learnrate = conf_info.data.learnrate
        conf_info.n_class = len(json.loads(net_info['datasets']))

        # define classifier
        utils.tfmsa_logger("[4]define classifier")
        classifier = learn.Estimator(model_fn=ConvCommonManager(conf_info).struct_cnn_layer,
                                     model_dir=netconf.nn_model_manager.get_model_save_path(nn_id),
                                     config = learn.RunConfig(save_checkpoints_secs=1))

        utils.tfmsa_logger("[5]predict result")
        y_predicted = [
            p['class'] for p in classifier.predict(
                x=np.array(predict_data, np.float32),
                input_fn=None,
                batch_size=100,
                as_iterable=True)
            ]
        return y_predicted
    except Exception as e:
        print("Error Message : {0}".format(e))
        raise Exception(e)