from tfmsacore import train
from tfmsacore import predict
from tfmsacore import data
from tfmsacore import netconf
import json

class TFMsa :
    """
    TO-DO: manager class provide all services , train, predict, conf change
    """

    def trainNerualNetwork(self,nn_id, nn_type, run_type):
        """
        train neuralnetwork on spark or local machine
        :param nn_id:
        :param nn_type:
        :param run_type:
        :return:
        """
        if(nn_type == "cnn" and run_type == "local"):
            return train.train_conv_network(nn_id)

        elif(nn_type == "cnn" and run_type == "spark"):
            return train.spark_train_conv_network(nn_id)
        else :
            return "cannot understand the request!"

    def predictNerualNetwork(self, nn_id, nn_type, run_type, predict_data):
        """
        predict neural network with given data
        :param nn_id:
        :param nn_type:
        :param run_type:
        :param predict_data:
        :return:
        """
        if(nn_type == "cnn"):
            return predict.predict_conv_network(nn_id, predict_data)
        else :
            return "cannot understand the request!"

    def createNeuralNetwork(self, info, conf):
        """
        create net neural network and conf for training
        :param req:
        :return:
        """
        info_data = data.JsonDataConverter().load_obj_json(str(info))

        try:
            netconf.create_new_network(info)
            netconf.save_conf(info_data.nnid, conf)
        except ValueError as e :
            return "create Neural Net Error"

        return "success"

    def updateNeuralNetwork(self, info, conf):
        """
        update net neural network and conf for training
        :param req:
        :return:
        """
        info_data = data.JsonDataConverter().load_obj_json(str(info))
        try:
            netconf.create_new_network(info)
            netconf.save_conf(info_data.nnid, conf)
        except ValueError as e :
            return "update Neural Net Error"

        return "success"

    def searchNeuralNetwork(self, info):
        """
        :param req:
        :return:
        """
        try:
            info_data = data.JsonDataConverter().load_obj_json(str(info))
            conf_result = netconf.load_ori_conf(info_data.nnid)
        except ValueError as e :
            return "search Neural Net Error"

        return conf_result

#TFMsa.trainNerualNetwork("cnn", "sample", "local")