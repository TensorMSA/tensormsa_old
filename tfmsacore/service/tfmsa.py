from tfmsacore import train
from tfmsacore import predict
from tfmsacore import data
from tfmsacore import utils
from tfmsacore import netconf
from tfmsarest import livy
import json, unicodedata


class TFMsa :
    """
    TO-DO: manager class provide all services , train, predict, conf change
    """
    def __init__(self):
        """
        TO-DO : only for the test purpose will be deleted
        """
        utils.tfmsa_logger("TFMsa Class Init ")

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
        info_data = utils.JsonDataConverter().load_obj_json(str(info))

        try:
            netconf.create_new_network(json.loads(info))
            netconf.remove_conf(info_data.nn_id)
            netconf.remove_trained_data(info_data.nn_id)
            netconf.save_conf(info_data.nn_id, conf)
        except ValueError as e :
            return {}

        return info_data.nn_id

    def updateNeuralNetwork(self, info, conf):
        """
        update net neural network and conf for training
        :param info:neural network general info for management
        :param conf:acutual strcture information of neural network
        :return: success of failure
        """
        info_data = utils.JsonDataConverter().load_obj_json(str(info))
        try:
            netconf.update_network(info_data)
            netconf.save_conf(info_data.nn_id, conf)
            return info_data.nn_id

        except Exception as e:
            raise Exception(e)


    def searchNeuralNetwork(self, info):
        """
        :param info:neural network general info for management
        :return:acutual strcture information of neural network
        """
        try:
            info_data = utils.JsonDataConverter().load_obj_json(str(info))
            conf_result = netconf.load_ori_conf(info_data.nn_id)
            return conf_result

        except Exception as e:
            raise Exception(e)



    def getNeuralNetConfig(self, nn_id, category):
        """
        :param info: neural network management key
        :return:config informaion of seleted one
        """
        try:
            retrun_data = netconf.filter_network_config(nn_id, category)
            return retrun_data

        except Exception as e:
            raise Exception(e)



    def createDataFrame(self, nn_id, table, data):
        """
        Insert data and analize categories
        (1) Spark session create
        (2) Create Table with request data
        (3) Find Distinct list of each Column set as category
        (4) Store it on nn_info again

        :param nn_id:neural network management id
        :param table:table id of data sets
        :param data:initial dataset for table
        :return:
        """
        try:
            nn_info = netconf.get_network_config(nn_id)
            livy_client = livy.LivyDfClientManager(2)
            livy_client.create_session()
            livy_client.create_table(table, data)
            json_obj = json.loads(str(nn_info['datadesc']).replace("'", "\""))
            cate_column_list = []
            for column in json_obj.keys():
                if(json_obj[column] == 'cate' or json_obj[column] == 'tag' or json_obj[column] == 'rank' ):
                    cate_column_list.append(column)

            dist_col_list = livy_client.get_distinct_column(table, cate_column_list)
            netconf.set_train_datasets(nn_id, str(dist_col_list))

            return "success"

        except Exception as e:
            raise Exception(e)
