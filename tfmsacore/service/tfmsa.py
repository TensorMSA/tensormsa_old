from tfmsacore.train.conv_train import train_conv_network
from tfmsacore.train.conv_train_spark import spark_train_conv_network
from tfmsacore.predict.conv_predict import predict_conv_network

class TFMsa :
    """
    TO-DO: manager class provide all services , train, predict, conf change
    """
    def __init__(self):
        """
        TO-DO : not sure ..
        """

    @staticmethod
    def trainNerualNetwork(nn_type, nn_id, run_type):
        if(type == "conv" & run_type == "local"):
            return train_conv_network(nn_id)

        elif(type == "conv" & run_type == "spark"):
            return spark_train_conv_network(nn_id)

        else :
            return "cannot understand the request!"


    @staticmethod
    def predictNerualNetwork(nn_type, nn_id):
        if(type == "conv"):
            return predict_conv_network(nn_id)

        else :
            return "cannot understand the request!"
