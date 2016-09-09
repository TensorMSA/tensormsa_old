from tfmsacore.train.conv_train import train_conv_network
from tfmsacore.train.conv_train_spark import spark_train_conv_network
from tfmsacore.predict.conv_predict import predict_conv_network
from tfmsacore.data.json_conv import JsonDataConverter as jc
from tfmsacore.netconf.nn_common_manager import NNInfoManager as  NNInfoManager

class TFMsa :
    """
    TO-DO: manager class provide all services , train, predict, conf change
    """

    def trainNerualNetwork(self,nn_id, nn_type, run_type):
        if(nn_type == "cnn" and run_type == "local"):
            return train_conv_network(nn_id)

        elif(nn_type == "cnn" and run_type == "spark"):
            return spark_train_conv_network(nn_id)
        else :
            return "cannot understand the request!"

    def predictNerualNetwork(self, nn_id, nn_type, run_type, predict_data):
        if(nn_type == "cnn"):
            return predict_conv_network(nn_id, predict_data)
        else :
            return "cannot understand the request!"

    def createNewNeuralNet(self, req):
        result = NNInfoManager().create_new_network(req)
        return result

#TFMsa.trainNerualNetwork("cnn", "sample", "local")