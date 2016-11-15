from sklearn import metrics
import tensorflow as tf
from tensorflow.contrib import learn
import numpy as np
from tfmsacore import netconf
from tfmsacore import utils
from TensorMSA import const
import json, math, copy
from tfmsacore.netcommon.conv_common import ConvCommonManager
from tfmsacore.netcommon.acc_eval_common import AccEvalCommon
from tfmsacore.netcommon.acc_eval_common import AccStaticResult
from tfmsacore import netcommon

def eval_conv_network(nn_id, samplenum = 0.1, samplemethod = 1):
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

        # TODO : need to change data loader to get sample data (not all data)
        if(const.TYPE_IMAGE == net_info['preprocess']):
            train_data_set, train_label_set = ConvCommonManager(conf_info).prepare_image_data(nn_id, net_info)
        elif(const.TYPE_DATA_FRAME == net_info['preprocess']):
            raise Exception("function not ready")
        elif(const.TYPE_TEXT == net_info['preprocess']):
            raise Exception("function not ready")
        else:
            raise Exception("unknown data type")

        # data size info change
        utils.tfmsa_logger("[5]modify data stuctor info")
        ConvCommonManager(conf_info).save_changed_data_info(nn_id, train_data_set)

        learnrate = conf_info.data.learnrate
        label_set = json.loads(net_info['datasets'])
        conf_info.n_class = len(label_set)

        # change to nummpy array
        train_x = np.array(train_data_set, np.float32)
        train_y = np.array(train_label_set, np.int32)

        # define classifier
        utils.tfmsa_logger("[6]define classifier")
        classifier = learn.Estimator(model_fn=ConvCommonManager(conf_info).struct_cnn_layer,
                                     model_dir=netconf.nn_model_manager.get_model_save_path(nn_id))

        # start train
        #TODO : need to find way to predict without fit
        utils.tfmsa_logger("[5]fit dummy")
        dummy_x = np.array([ConvCommonManager(conf_info).create_dummy_matrix(len(train_x[0]))], np.float32)
        dummy_y = np.array(netcommon.convert_to_index(json.loads(net_info['datasets'])), np.int32)
        classifier.fit(dummy_x, dummy_y, steps=int(1))

        # start train
        utils.tfmsa_logger("[8]evaluate prediction result")
        counter = 0
        acc_result_obj = AccStaticResult()
        for p in classifier.predict(x=np.array(train_x, np.float32),batch_size=1,as_iterable=True):
            acc_result_obj = AccEvalCommon(nn_id).set_result(acc_result_obj, label_set[train_y[counter]], label_set[int(p['class'])])
            counter = counter + 1
        return len(train_y)

    except Exception as e:
        print("Error Message : {0}".format(e))
        raise Exception(e)