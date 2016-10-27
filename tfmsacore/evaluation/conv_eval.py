# from tfmsacore.utils.logger import tfmsa_logger
# from tfmsacore import netconf
# import numpy as np
# import tflearn as tflearn
# from tflearn.layers.conv import conv_2d, max_pool_2d
# from tflearn.layers.core import input_data, dropout, fully_connected
# from tflearn.layers.estimator import regression
# from tflearn.layers.normalization import local_response_normalization
# from tfmsacore.data.data_master import DataMaster
# from tfmsacore.data.table_preprocess import DFPreProcessor
# from tfmsacore.utils.json_conv import JsonDataConverter as jc
# from tfmsacore import data as td
# from tfmsacore import netconf
# from tfmsacore import utils
# from tfmsacore.utils import tfmsa_logger
#
# class CNNEval:
#     """
#     Convolutional Neuralnetwork Evaluation Class
#     """
#     def __int__(self):
#         """
#         initialize variables
#         :return:
#         """
#         tfmsa_logger("init CNN Evaluation")
#         self.nn_id = None
#         self.sample_percent = None
#         self.sample_num = None
#         self.sample_method = None
#         self.test_pass = None
#         self.test_fail = None
#         self.acc = None
#
#     def eval_model(self, nn_id, sample_percent, sample_method):
#         """
#         evaluate accuracy with extracting random sample data
#         :param nn_id:
#         :param sample_percent:
#         :param sample_method:
#         :return:
#         """
#         self.nn_id = nn_id
#         self.sample_percent = float(sample_percent)
#         self.sample_num = int(0)
#         self.sample_method = sample_method
#         self.test_pass = int(0)
#         self.test_fail = int(0)
#         self.acc = float(0)
#
#         #get test data from spark
#         self.save_condition(sample_percent, sample_method)
#         self.test_cnn()
#         self.save_result()
#
#     def save_condition(self, sample_percent, sample_method):
#         """
#         save test condition on database
#         :return:
#         """
#         jd = jc.load_obj_json("{}")
#         jd.samplepercent = sample_percent
#         jd.samplemethod = sample_method
#         jd.nn_id = self.nn_id
#         netconf.update_network(jd)
#
#     def save_result(self):
#         """
#         save test result on database
#         :return:
#         """
#         tfmsa_logger("sample_num  {0}".format(self.sample_num))
#         tfmsa_logger("acc  {0}".format(self.acc))
#         tfmsa_logger("test_pass  {0}".format(self.test_pass))
#         tfmsa_logger("test_fail  {0}".format(self.test_fail))
#
#         jd = jc.load_obj_json("{}")
#         jd.samplepercent = self.sample_percent
#         jd.samplemethod = self.sample_method
#         jd.samplenum = self.sample_num
#         jd.testpass = self.test_pass
#         jd.testfail = self.test_fail
#         jd.acc = self.acc
#         jd.nn_id = self.nn_id
#         netconf.update_network(jd)
#
#     def compare_result(self, data1, data2):
#         """
#         compare original data and predict data
#         :param data1:
#         :param data2:
#         :return:
#         """
#         for idx in range(0, len(data2)):
#             if(data1[idx].index(max(data1[idx])) == data2[idx].index(max(data2[idx]))):
#                 self.test_pass += 1
#             else:
#                 self.test_fail += 1
#
#         self.sample_num = self.test_pass + self.test_fail
#         self.acc = round(float(self.test_pass) / self.sample_num, 3)
#
#
#     def test_cnn(self):
#         """
#         test cnn and get predict result
#         :return:
#         """
#         try:
#             tfmsa_logger("start Evaluation....")
#             # load NN conf form db
#             conf = netconf.load_conf(self.nn_id)
#
#             # modify predict fit to tarin
#             sp_loader = DFPreProcessor().get_eval_data(self.nn_id)
#
#             # set spaces for input data
#             datalen = conf.data.datalen
#             matrix = conf.data.matrix
#             learnrate = conf.data.learnrate
#             request_x = np.reshape(sp_loader.m_train, (-1, matrix[0], matrix[1], 1))
#             request_y = sp_loader.m_tag
#
#             # create network conifg
#             num_layers = len(conf.layer)
#             for i in range(0, num_layers):
#
#                 data = conf.layer[i]
#                 if (data.type == "input"):
#                     network = input_data(shape=[None, matrix[0], matrix[1], 1], name='input')
#                     network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active),
#                                       regularizer=data.regualizer)
#                     network = max_pool_2d(network, data.maxpoolmatrix)
#                     network = local_response_normalization(network)
#
#                 elif (data.type == "cnn"):
#                     network = conv_2d(network, data.node_in_out[1], data.cnnfilter, activation=str(data.active),
#                                       regularizer=data.regualizer)
#                     network = max_pool_2d(network, data.maxpoolmatrix)
#                     network = local_response_normalization(network)
#
#                 elif (data.type == "drop"):
#                     network = fully_connected(network, data.node_in_out[0], activation=str(data.active))
#                     network = dropout(network, int(data.droprate))
#                     network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
#                     network = dropout(network, int(data.droprate))
#
#                 elif (data.type == "out"):
#                     network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
#                     network = regression(network, optimizer='adam', learning_rate=learnrate,
#                                          loss='categorical_crossentropy', name='target')
#
#                 elif (data.type == "fully"):
#                     network = fully_connected(network, data.node_in_out[1], activation=str(data.active))
#
#                 else:
#                     raise SyntaxError("there is no such kind of nn type : " + str(data.active))
#
#             # set net conf to real tensorflow
#             model = tflearn.DNN(network, tensorboard_verbose=0)
#
#             # restore model and start predict with given data
#             model = netconf.nn_data_manager.load_trained_data(self.nn_id, model)
#             result = model.predict(request_x)
#
#             self.compare_result(request_y, result)
#
#             tfmsa_logger("End Evaluation with result : {0}".format(self.acc))
#             return self.acc
#
#         except SyntaxError as e:
#             tfmsa_logger("Error while Evaluation  : {0}".format(e))
#             return e