from tfmsacore import train
from tfmsacore import predict
from tfmsacore import data
from tfmsacore import netconf
import json

class TFMsa :
    """
    TO-DO: manager class provide all services , train, predict, conf change
    """
    def __init__(self):
        """
        TO-DO : only for the test purpose will be deleted
        """
        netconf.test_data_move()

    def trainNerualNetwork(self,nn_id, nn_type, run_type, epoch, testset):
        """
        train neuralnetwork on spark or local machine
        :param nn_id: neural network id managed on out framework
        :param nn_type: type of neural network like 'cnn', 'dnn', 'rnn'
        :param run_type: local or spark
        :parmam epoch : number of training iterations
        :param testset : number of dataset to use on test
        :return: accuracy of train neural network result
        """
        if(nn_type == "cnn" and run_type == "local"):
            return train.train_conv_network(nn_id, epoch, testset)

        elif(nn_type == "cnn" and run_type == "spark"):
            return train.spark_train_conv_network(nn_id, epoch, testset)
        else :
            return [0.0]

    def predictNerualNetwork(self, nn_id, nn_type, run_type, predict_data):
        """
        predict neural network with given data
        :param nn_id: neural network id managed on out framework
        :param nn_type: type of neural network like 'cnn', 'dnn', 'rnn'
        :param run_type: local or spark
        :param predict_data: request data to predict with neural network
        :return: list data set of neural net predict result
        """
        if(nn_type == "cnn"):
            return predict.predict_conv_network(nn_id, predict_data)
        else :
            return []

    def createNeuralNetwork(self, info, conf):
        """
        create net neural network and conf for training
        :param info:neural network general info for management
        :param conf:acutual strcture information of neural network
        :return:success of failure
        """
        info_data = data.JsonDataConverter().load_obj_json(str(info))

        try:
            netconf.create_new_network(json.loads(info))
            netconf.save_conf(info_data.nnid, conf)
        except ValueError as e :
            return "error"

        return info_data.nnid

    def updateNeuralNetwork(self, info, conf):
        """
        update net neural network and conf for training
        :param info:neural network general info for management
        :param conf:acutual strcture information of neural network
        :return: success of failure
        """
        info_data = data.JsonDataConverter().load_obj_json(str(info))
        try:
            netconf.create_new_network(json.loads(info))
            netconf.save_conf(info_data.nnid, conf)
        except ValueError as e :
            return "error"

        return info_data.nnid

    def searchNeuralNetwork(self, info):
        """
        :param info:neural network general info for management
        :return:acutual strcture information of neural network
        """
        try:
            info_data = data.JsonDataConverter().load_obj_json(str(info))
            conf_result = netconf.load_ori_conf(info_data.nnid)
        except ValueError as e :
            return {}

        return conf_result

#TFMsa.trainNerualNetwork("cnn", "sample", "local")