import tensorflow as tf
from tensorflow.contrib import learn
from tfmsacore.data.image_manager import ImageManager
from tfmsacore import utils
from tfmsacore import netcommon
from tfmsacore import netconf
import json, math
from tfmsacore.utils import CusJsonEncoder

class ConvCommonManager:
    """

    """
    def __init__(self, conf_info):
        self.conf = conf_info

    def prepare_image_data(self, nn_id, net_info):
        """
        prepare image type data
        convert image to analizerble array
        :param nn_id:
        :return:
        """

        # check current data pointer
        utils.tfmsa_logger("[1]check current data pointer")
        """
        TO-DO : case when data size is big
        """
        # get train data from HDFS
        utils.tfmsa_logger("[2]load data from hdfs")
        row_data_arr = ImageManager().load_data(net_info['dir'], net_info['table'], "0", "10")

        # conver image to array
        utils.tfmsa_logger("[3]convert image to array")
        out_index = json.loads(net_info['datasets'])
        train_data_set = []
        train_label_set = []
        for row_data in row_data_arr:
            train_data_set.append(json.loads(str(row_data['bt'],'utf-8')))
            train_label_set.append(netcommon.return_index_position(out_index, str(row_data['label'], 'utf-8')))
        return train_data_set, train_label_set

    def prepare_test_image_data(self, nn_id, net_info):
        """
        prepare image type data for test
        convert image to analizerble array
        :param nn_id:
        :return:
        """

        # check current data pointer
        utils.tfmsa_logger("[1]check current data pointer")
        """
        TO-DO : case when data size is big
        """
        # get train data from HDFS
        utils.tfmsa_logger("[2]load data from hdfs")
        row_data_arr = ImageManager().load_data("test_schema_" + net_info['dir'], net_info['table'], "0", "10")

        # conver image to array
        utils.tfmsa_logger("[3]convert image to array")
        out_index = json.loads(net_info['datasets'])
        train_data_set = []
        train_label_set = []
        for row_data in row_data_arr:
            train_data_set.append(json.loads(str(row_data['bt'],'utf-8')))
            train_label_set.append(netcommon.return_index_position(out_index, str(row_data['label'], 'utf-8')))
        return train_data_set, train_label_set

    def struct_cnn_layer(self, train_data_set, train_label_set):
        """
        dynamically struct cnn
        :param num_layers:
        :param conf_info:
        :return:
        """
        conf_info = self.conf
        num_layers = len(conf_info.layer)
        matrix = conf_info.data.matrix.copy()
        train_data_set = tf.reshape(train_data_set, [-1, matrix[0], matrix[1], 1])
        curren_matrix = matrix
        curren_matrix_num = 0

        train_label_set = tf.one_hot(train_label_set, int(conf_info.n_class), 1, 0)
        for i in range(0, int(num_layers)):
            data = conf_info.layer[i]
            utils.tfmsa_logger("[{0}]define layers : {1}".format(i, data.type))
            if (data.type == "cnn" and i ==0):
                train_data_set = tf.reshape(train_data_set, [-1, matrix[0], matrix[1], 1])
                network = tf.contrib.layers.conv2d(train_data_set,
                                                   num_outputs=data.node_in_out[1],
                                                   kernel_size=data.cnnfilter,
                                                   activation_fn=self.get_activation(str(data.active)))
                network = tf.nn.max_pool(network,
                                         ksize=[1, data.maxpoolmatrix[0], data.maxpoolmatrix[1], 1],
                                         strides=[1, data.maxpoolstride[0], data.maxpoolstride[1], 1],
                                         padding=data.padding)

                curren_matrix = self.mat_size_cal(curren_matrix, data.padding, data.maxpoolmatrix, data.maxpoolstride)
                curren_matrix_num = data.node_in_out[1]
            elif (data.type == "cnn"):
                network = tf.contrib.layers.conv2d(network,
                                                   num_outputs=data.node_in_out[1],
                                                   kernel_size=data.cnnfilter,
                                                   activation_fn=self.get_activation(str(data.active)))
                network = tf.nn.max_pool(network, ksize=[1, data.maxpoolmatrix[0], data.maxpoolmatrix[1], 1],
                                         strides=[1, data.maxpoolstride[0], data.maxpoolstride[1], 1],
                                         padding=data.padding)
                curren_matrix = self.mat_size_cal(curren_matrix, data.padding, data.maxpoolmatrix, data.maxpoolstride)
                curren_matrix_num = data.node_in_out[1]
            elif (data.type == "reshape"):
                network = tf.reshape(network, [-1, curren_matrix[0] * curren_matrix[1] * curren_matrix_num])
            elif (data.type == "drop"):
                data_num = curren_matrix[0] * curren_matrix[1] * curren_matrix_num
                network = tf.contrib.layers.dropout(
                    tf.contrib.layers.legacy_fully_connected(
                        network, data_num, weight_init=None,
                        activation_fn=self.get_activation(str(data.active))),
                    keep_prob=float(data.droprate)
                )
            elif (data.type == "out"):
                network = learn.models.logistic_regression(x=network, y=train_label_set)
            else:
                raise SyntaxError("there is no such kind of layer type : " + str(data.type))

        with tf.name_scope('loss'):
            prediction, loss = (network)

        with tf.name_scope('train_op'):
            train_op = tf.contrib.layers.optimize_loss(
            loss, tf.contrib.framework.get_global_step(), optimizer='Adagrad',
            learning_rate=0.1)
        return {'class': tf.argmax(prediction, 1), 'prob': prediction}, loss, train_op


    def get_activation(self, activitaion):
        """
        return activation functions with str activation type
        :param activitaion:
        :return:
        """
        if activitaion == 'relu':
            return tf.nn.relu
        elif activitaion == 'softmax':
            return tf.nn.softmax('float32')
        else :
            return tf.nn.relu

    def mat_size_cal(self, curren_matrix, padding, max_pool_matrix, max_pool_stride):
        """
        resize each matrix size
        :param curren_matrix:
        :param padding:
        :param max_pool:
        :return:
        """
        if(padding == 'SAME'):
            curren_matrix[0] = int(curren_matrix[0]/max_pool_stride[0])
            curren_matrix[1] = int(curren_matrix[1]/max_pool_stride[1])
        else:
            curren_matrix[0] = int(curren_matrix[0]/max_pool_stride[0] - 1)
            curren_matrix[1] = int(curren_matrix[1]/max_pool_stride[1] - 1)

        return curren_matrix

    def save_changed_data_info(self, nn_id, train_data_set):
        """
        save train data size related information on db
        :param nn_id: neural network management id
        :param spark_loader: spark_loader class object
        :return: None
        """
        train_len = len(train_data_set[0])
        json_conf = self.conf
        json_conf.data.datalen = train_len
        len_sqrt = int(math.ceil(math.sqrt(train_len)))

        flag = False
        for i in range(0, len_sqrt):
            for x in range(0, len_sqrt):
                if(int(json_conf.data.datalen) == (len_sqrt + x) * (len_sqrt - i)):
                    json_conf.data.matrix = [(len_sqrt + x), len_sqrt - i]
                    flag = True

        if(flag == False):
            json_conf.data.matrix = [train_len, 1]

        netconf.save_conf(nn_id, json.dumps(json_conf, cls=CusJsonEncoder))


    def create_dummy_matrix(self, data_len):
        """

        :param train_len:
        :param label_len:
        :return:
        """
        dummyarray = []
        for x in range(int(data_len)):
            dummyarray.append(0)
        return  dummyarray

